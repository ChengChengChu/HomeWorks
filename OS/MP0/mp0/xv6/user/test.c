#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"

char* get_filename(char *path) {
    char *p;
    for (p=path+strlen(path); p>=path && *p != '/'; p--);
    p++;
    return p;
}

void find(char *path, char *name) {
    printf("%s\n", path);
    char buf[512], *p;
    int fd;
    struct stat st;
    struct dirent de;

    if ((fd=open(path, 0)) < 0) {
        fprintf(2, "find: cannot open %s\n", path);
        return;
    }

    if (fstat(fd, &st) < 0) {
        fprintf(2, "find: cannot stat %s\n", path);
        close(fd);
        return;
    }

    switch (st.type) {
    case T_FILE:
        p = get_filename(path);
        printf("Find File : %s !!!!!\n", p);
        if (!strcmp(p, name))
            printf("%s\n", path);
        break;
    
    case T_DIR:
        while(read(fd, &de, sizeof(de)) == sizeof(de)) {
            if(strlen(path) + 1 + DIRSIZ + 1 > sizeof buf){
                printf("find: path too long\n");
                break;
            }
            if (de.inum == 0)
                continue;
            if (!strcmp(de.name, ".") || !strcmp(de.name, ".."))
                continue;
            printf("Before strcpy :\npath : %s\nbuf : %s\n", path, buf);
            strcpy(buf, path);
            printf("After strcpy :\npath : %s\nbuf : %s\n", path, buf);
            p = buf + strlen(buf);
            printf("p : %s\n", p);
            *p++ = '/';
            printf("p : %s\n", p);
            memmove(p, de.name, DIRSIZ);
            printf("p : %s\n", p);
            printf("==================\n");
            p[DIRSIZ] = '\0';
            find(buf, name);
        }
        break;
    }
    close(fd);
    return;
}

void main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(2, "Usage: find <path> <name>\n");
        exit(1);
    }

    find(argv[1], argv[2]);
    exit(0);
}
