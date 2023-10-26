### Android命令大全

#### adb命令

##### 1.查看CPU架构

> adb [-s device] shell getprop ro.product.cpu.abi

`-s`多个设备时，用于指定指定设备

如：adb -s S4D6AQ5TKBSO8DEQ shell getprop ro.product.cpu.abi

返回：arm64-v8a或者armeabi-v7a

##### 2.查看设备

> adb devices

##### 3.选择设备

> adb -s 设备名称

##### 4.安装apk

> adb [-s 设备名称] install -r [-d]xxx.apk

`-s`多个设备时，用于指定安装在哪个设备上；

`-r`安装的apk存在时，先进行卸载再安装；

`-d`版本降级安装，即安装低版本；

##### 5.卸载APP

> adb [-s 设备名称] uninstall app包名

示例：`adb -s S9B7N17626022785 uninstall com.zhh.demo`

##### 6.查看手机型号

> adb shell getprop ro.product.model

##### 7.查看电池状况

> adb shell dumpsys battery

其中：`scale`代表最大电量，`level`代表当前电量。

##### 8.查看手机分辨率

> adb shell wm size

##### 9.查看手机屏幕密度

> adb shell wm density

##### 10.查看显示屏参数

> adb shell dumpsys window displays

##### 11.查看Android_id

> adb shell settings get secure android_id

##### 12.查看Android系统版本

> adb shell getprop ro.build.version.release

#### aapt命令

##### 1.列出压缩文件(zip,jar,apk)中的目录内容

> aapt l[ist] [-v] [-a] file.{zip,jar,apk}

##### 2.查看apk中各种详细信息

> aapt d[ump] [--values] [--include-meta-data] WHAT file.{apk} [asset [asset ...]]

> strings          Print the contents of the resource table string pool in the APK.
> badging          Print the label and icon for the app declared in APK.
> permissions      Print the permissions from the APK.
> resources        Print the resource table from the APK.
> configurations   Print the configurations in the APK.
> xmltree          Print the compiled xmls in the given assets.
> xmlstrings       Print the strings of the given compiled xml assets.

##### 3.编译资源打包资源文件

> aapt p[ackage] [-d][-f][-m][-u][-v][-x][-z] -M AndroidManifest.xml

android 编译资源打包资源文件的命令。

- -d:包括一个或多个设备资源,由逗号分隔;
- -f:覆盖现有的文件命令,加上后编译生成直接覆盖目前已经存在的R.java;
- -m:使生成的包的目录放在-J参数指定的目录;
- -u:更新现有的包 u = update;
- -v:详细输出,加上此命令会在控制台输出每一个资源文件信息,R.java生成后还有注释。
- -x:创建扩展资源ID;
- -z:需要本地化的资源属性标记定位。
- -M:AndroidManifest.xml的路径
- -0:指定一个额外的扩展. apk文件将不会存储压缩
- -g:制定像素迫使图形的灰度
- -j:指定包含一个jar或zip文件包,这个命令很特别
- –debug-mode:指定的是调试模式下的编译资源;
- –min-sdk-versopm VAL:最小SDK版本 如是7以上 则默认编译资源的格式是 utf-8
- –target-sdk-version VAL:在androidMainfest中的目标编译SDK版本
- –app-version VAL:应用程序版本号
- –app-version-name TEXT:应该程序版本名字;
- –custom-package VAL:生成R.java到一个不同的包
- –rename-mainifest-package PACKAGE:修改APK包名的选项;
- –rename-instrumentation-target-package PACKAGE:重写指定包名的选项;
- –utf16:资源编码修改为更改默认utf – 16编码;
- –auto-add-overlay:自动添加资源覆盖
- –max-res-version:最大资源版本
- -I:指定的SDK版本中android.jar的路径
- -A:assert文件夹的路径
- -G:一个文件输出混淆器选项,后面加文件逗号隔开.
- -P:指定的输出公共资源,可以指定一个文件 让资源ID输出到那上面;
- -S:指定资源目录 一般是 res
- -F:指定把资源输出到 apk文件中
- -J:指定R.java输出的路径
- raw-file-dir:附加打包进APK的文件

##### 4.文件中删除

> aapt r[emove] [-v] file.{zip,jar,apk} file1 [file2 ...]

##### 5.添加一个指定的文件

> aapt a[dd] [-v] file.{zip,jar,apk} file1 [file2 ...]

##### 6.对资源文件夹进行处理

> aapt c[runch] [-v] -S resource-sources ... -C output-folder ...

对多个或者单个资源文件夹进行处理，并且将结果保存在输出文件夹中

##### 7.预处理一个文件

> aapt s[ingleCrunch] [-v] -i input-file -o outputfile

预处理一个文件

#### 打包相关命令

##### 1.jar转dex文件

> dx --dex --output [输出dex] [输入的jar]

##### 2.apktool反编译与回编译

> 反编译：apktool d -o [输出目录] [apk]
> 
> 回编译：apktool b -o [输出apk] [回编译目录]

##### 3.apk对齐命令

> 命令：zipalign -v -p 4 [输入的apk] [对齐后的apk]

#### apksigner签名命令

##### 1.签名

> apksigner sign --ks [签名文件] --ks-key-alias [alias名字] --min-sdk-version 21 --ks-pass pass:[keystore密码] --key-pass pass:[key密码] --v1-signer-name CERT --out [输出apk] [输入apk]

若需修改v1 v2 v3签名可增加`--v1-signing-enabled false/true`

- v1 - `--v1-signing-enabled`
- v2 - `--v2-signing-enabled`
- v3 - `--v3-signing-enabled`

`--v1-signer-name [名称]` 签名后修改META-INF中.RSA和.SF文件名称

##### 2.查看apk签名信息

>  apksigner verify --verbose [apk]

#### keytool命令

##### 1.创建签名文件



##### 2.查看签名文件

- 查看MD5
  
  方式一(该方式不是很有效果，建议采用方式二)：
  
  > keytool -exportcert -keystore [签名文件] | openssl dgst -md5
  
  方式二：
  
  > ./gradlew signingReport
  
  或直接运行gradle的Task任务
  
  ![](https://upload-images.jianshu.io/upload_images/11268516-f18b001c3f27ebd3.png?imageMogr2/auto-orient/strip|imageView2/2/w/1120/format/webp)

- 列出签名信息
  
  > keytool -v -list -keystore [签名文件]
  
  > keytool -v -list -keystore [签名文件] -storepass "秘钥"

- 查看签名文件公钥
  
  > keytool -list -rfc --keystore [签名文件] | openssl x509 -inform pem -pubkey
