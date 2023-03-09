#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"

char* file_name(char* path){
    char* p;
    for (p = path + strlen(path); p >= path && *p != '/'; p --);
    p ++;
    return p;
}

int dir_count, file_count;

void mp0(char* path, char* key){
    char buf[512], *p, *find_key;
    int fd, key_count = 0;
    struct stat st;
    // stat :  DIR or DEVICE or FILE
    struct dirent de;

    // de : file_name, inum
    if ((fd = open(path, 0)) < 0) {
        // printf("%d\n", fd);
        // printf("Here %s\n", path);
        fprintf(2, "%s [error opening dir]\n", path);
        //printf("=================\n");
        return;
    }
    if (fstat(fd, &st) < 0) {
        fprintf(2, "mp0 : cannnot stat file %s.\n", path);
    }
    for (find_key = path + strlen(path); find_key >= path; find_key --) {
        if (*find_key == *key) {
            key_count += 1;
        }
    }
    // print answer
    printf("%s %d\n", path, key_count);
    switch (st.type)
    {
    case T_FILE:
        file_count += 1;
        // printf("find file %s in %s !!!\n", file_name(path), path);
        break;
    case T_DIR :
        dir_count += 1;
        // printf("file : %s\n", path);
        while (read(fd, &de, sizeof(de)) == sizeof(de)) {
            if (strlen(path) + 1 + DIRSIZ + 1 > 512) {
                printf("find path too long !\n");
            }
            if (de.inum == 0) continue;
            if (!strcmp(de.name, ".") || !strcmp(de.name, "..")) continue;

            strcpy(buf, path);
            p = buf + strlen(buf);
            *p ++ = '/';
            memmove(p, de.name, DIRSIZ);
            p[DIRSIZ] = '\0';
            mp0(buf, key);
        }
        break;
    
    default:
        break;
    }
    close(fd);
}


int main(int argc, char* argv[]) {
    if (argc < 3) {
        fprintf(2, "mp0 : not enough argumenrs.\n");
        // return;
    }

    int pid, p[2], status;
    pipe(p);
    if ((pid = fork()) < 0) {
        fprintf(2, "mp0 : error forking a child.\n");
    } 
    else if (pid == 0) {
        // child process
        dir_count = file_count = 0;
        mp0(argv[1], argv[2]);
        close(0);
        write(p[1], &file_count, sizeof(int));
        write(p[1], &dir_count, sizeof(int));
        exit(0);
    }
    else {
        // parent
        wait(&status);
        int result;
        for (int i = 0; i < 2; i ++) {
            read(p[0], &result, sizeof(int));
            if (i == 0) {
                file_count = result;
            }
            else {
                dir_count = result;
            }
        }

        if (dir_count >= 1) {
            printf("\n%d directories, %d files\n", dir_count - 1, file_count);
        }
        else {
            printf("\n%d directories, %d files\n", dir_count, file_count);
        }
        

    }
    exit(0);
}