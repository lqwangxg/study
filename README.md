# study
# python study like a child.
# first time write readme comment by browser. just a test. -- 2017/10/06 11/42.

About Docker.
Lesson1: https://zhuanlan.zhihu.com/p/32643685
  Difference of Image and Container. 
  How to build a image from a basic image of ubuntu.
  构建Image的4中方式，
  1，docker run开一个空的容器，手动输入命令，然后Commit成一个镜像。
  2，docker run 空容器 + 导入文件
  3，基于dockerfile build成的镜像。
  4，dockerfile + configuration management
  
  Docker分层。写时复制。
-----------------------------------------
git命令示例
$ git clone git://github.com/git/hello-world.git
$ cd hello-world
$ (edit files)
$ git add (files)
$ git commit -m 'Explain what I changed'  #(local)
$ git format-patch origin/master
$ git push           #(remote)
$ git status

$ cd (project-directory)
 ——————————————————————————————————————————————————————————
$ git init
$ (add some files)
$ git add .
$ git commit -m 'Initial commit' 
$ git status

IBM Shifter介绍：高性能计算集群下的docker应用
https://www.ibm.com/developerworks/cn/linux/l-panxun-shifter-compute-container/index.html
