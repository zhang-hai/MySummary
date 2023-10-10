### 本地新建工程上传到远端

> git init
> git add README.md
> git commit -m "first commit"
> 
> //若分支不是master，则需要执行下一行命令创建新分支，如：main
> 
> git branch -M main
> git remote add origin git@github.com:zhang-hai/JetpackDemo.git
> git push -u origin 分支名称

### pick单次提交

> git cherry-pick <commitHash>  

### git删除远程仓库的文件或目录

> git rm -r --cached a/2.txt //删除a目录下的2.txt文件   删除a目录git rm -r --cached a
> git commit -m "删除a目录下的2.txt文件" 
> git push

---------------------------------------------------------------

### git分支相关

#### 创建分支

> git branch <新分支名称>

#### 创建分支并切换到新建的分值

> git checkout -b <新分支名称>

#### 给新分支添加注释

> git config branch.[branchName].description '这是注释'

#### 查看分支的注释

> git config branch.[branchName].description

#### 将新建分支推送到远端

> git push --set-upstream origin <新分支名称>

#### 删除分支

##### 本地分支

> git branch -d/--delete <分支名称>

##### 远端分支

> git push origin -d/--delete <分支名称>

#### 查看分支创建时间

> git reflog show --date=iso <branch/name>

-----------------------------------------------------------

### git Tag相关

#### 创建Tag

> git tag -a <tagName> -m <"my tag">

#### 同步Tag到远程服务器

##### 单个Tag

> git push origin <tagName>  

##### 所有Tag

> git push origin --tags

#### 删除Tag

##### 本地tag

> git tag -d tag-name

##### 远程tag

> git push origin :refs/tags/tag-name

#### 显示所有Tag及备注

> git tag -n    

-----------------------------------------------------------

### git修改用户配置信息

查询名称：git config --gloable user.name 
设置名称：git config --gloable user.name "名字"
查询email地址：git config --gloable user.email
设置email地址：git config --gloable user.email "邮箱地址"

-----------------------------------------------------------
