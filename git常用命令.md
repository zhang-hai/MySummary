### �����½������ϴ���Զ��

> git init
> git add README.md
> git commit -m "first commit"
> 
> //����֧����master������Ҫִ����һ��������·�֧���磺main
> 
> git branch -M main
> git remote add origin git@github.com:zhang-hai/JetpackDemo.git
> git push -u origin ��֧����

### pick�����ύ

> git cherry-pick <commitHash>  

### gitɾ��Զ�ֿ̲���ļ���Ŀ¼

> git rm -r --cached a/2.txt //ɾ��aĿ¼�µ�2.txt�ļ�   ɾ��aĿ¼git rm -r --cached a
> git commit -m "ɾ��aĿ¼�µ�2.txt�ļ�" 
> git push

---------------------------------------------------------------

### git��֧���

#### ������֧

> git branch <�·�֧����>

#### ������֧���л����½��ķ�ֵ

> git checkout -b <�·�֧����>

#### ���·�֧���ע��

> git config branch.[branchName].description '����ע��'

#### �鿴��֧��ע��

> git config branch.[branchName].description

#### ���½���֧���͵�Զ��

> git push --set-upstream origin <�·�֧����>

#### ɾ����֧

##### ���ط�֧

> git branch -d/--delete <��֧����>

##### Զ�˷�֧

> git push origin -d/--delete <��֧����>

#### �鿴��֧����ʱ��

> git reflog show --date=iso <branch/name>

-----------------------------------------------------------

### git Tag���

#### ����Tag

> git tag -a <tagName> -m <"my tag">

#### ͬ��Tag��Զ�̷�����

##### ����Tag

> git push origin <tagName>  

##### ����Tag

> git push origin --tags

#### ɾ��Tag

##### ����tag

> git tag -d tag-name

##### Զ��tag

> git push origin :refs/tags/tag-name

#### ��ʾ����Tag����ע

> git tag -n    

-----------------------------------------------------------

### git�޸��û�������Ϣ

��ѯ���ƣ�git config --gloable user.name 
�������ƣ�git config --gloable user.name "����"
��ѯemail��ַ��git config --gloable user.email
����email��ַ��git config --gloable user.email "�����ַ"

-----------------------------------------------------------
