###APK瘦身

#### 一、了解APK结构
APK文件由一个Zip压缩文件组成，包含了构成应用的所有文件。包括：Java类文件、资源文件和已编译资源文件

APK包含目录结构：

- META-INF/:包含CERT.SF和CERT.RSA签名文件，以及MANIFEST.MF清单文件。
- assets/：包含应用的资源，应用可以使用AssetManager对象检索这些资源。
- res/:包含未编译到resources.arsc中的资源
- lib/:包含特定于处理器软件层的以便以代码。含支持各cpu架构的so文件。
- resources.arsc:包含已编译的资源文件。
- classes.dex：包含一Dalvik/ART虚拟机可理解的DEX文件。
- AndroidManifest.xml：包括核心Android清单文件。



#### 二、采用App Bundle上传应用，目前Google Play支持该种方式上传，国内各平台暂未支持；

#### 三、使用Android Size Analyzer 工具检测

安装：
File ->Setting -> Plugins -> Marketplace，搜索“Android Size Analyzer”,查找到后，进行安装

使用：
Analyze > Analyze App Size 对当前项目运行应用大小分析。分析了项目后，系统会显示一个工具窗口，包含了如何缩减应用大小的建议。


#### 四、减少包体积方向

#####1.缩减资源数量和大小

	
- 移除未使用的资源，可以借助Andnroid Studio 自带的lint工具对res/中资源引用分析，可以检测出未被引用到的资源。检测出未引用资源时会进行提示，但不会删除。
	> 注：lint工具不会对assets/文件夹、通过反射引用的资源或链接至应用的库文件进行扫描。
	
- 移除引入代码库中未使用到的资源。在build.gradle中配置shrinkResources，则Gradle可以自动移除资源，如下
	 android {
	        // Other settings
	
	        buildTypes {
	            release {
	                minifyEnabled true
	                shrinkResources true
	                proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
	            }
	        }
    	}
- 减少库中的资源使用量

	在开发过程中使用外部库时，可能包含应用不需要的对象和方法。如果库允许修改的情况下，可编辑库文件，使其适合移动设备的库。同时也可以清理库中一些不必要代码

- 屏幕适配，仅支持特定密度

	在当前的Android设备中，包含了各种屏幕密度。在Android 4.4及以上版本中，框架支持各种密度：ldpi、mdpi、tvdpi、hdpi、xhdpi、xxhdpi和xxxhdpi。但在实际开发中无需适配每个密度。

- 使用可绘制对象

	某些图片不需要静态图片资源时，可以在程序运行时动态绘制图片。如：Drawable对象，使用shape

- 资源重复利用

	资源能重复使用的尽量重复使用，比如：向下箭头，可通过旋转获取到向上箭头，这样就节约一个图片资源；

	可以通过Android提供的使用更改资源颜色api，比如：android:tint和android:tintMode属性（Android 5.0以上版本），对于较低的版本可以使用ColorFilter类。

- 采用代码进行渲染

	对于简单的，可通过程序来渲染图片

- 对PNG jpeg图片资源进行压缩
	
	一般情况下aapt工具可在编译过程中通过无损压缩来优化放置在res/drawable/中的图片资源。
	> aapt的限制
	> 
	> asset目录中的资源文件不会被压缩
	> 
	> 图片使用256中或更少的颜色，aapt工具才进行优化
	> 
	> aapt工具可能会扩充已压缩的png图片。

	对png资源，建议使用[pngcrush](https://pmt.sourceforge.io/pngcrush/)或者[tinypng](https://tinypng.com/)进行压缩，同时不损失画质。

	对JPEG资源，可以使用[guetzli](https://github.com/google/guetzli)和[tinypng](https://tinypng.com/)等工具进行压缩

- 使用WebP文件格式

	Webp格式属于有损压缩，在对质量要求不是很高的情况可以采用该方式。

- 使用矢量图形

	对于小图标，可以采用矢量图形，创建于分辨率无关的图标和其他可伸缩媒体。
	矢量图在Android中以VectorDrawable对象的形式。

	> 注：系统渲染VecotrDrawable对象需要花费时间，对于较大的图片，渲染时间则更长。因此，建议小图片使用该方式。

- 将矢量图形用于动画图片

	尽量避免使用AnimationDrawable帧动画，因为每一帧都是一个图片，这样会大大增加APK大小。
	建议采用AnimatedVectorDrawableCompat创建动画矢量资源。

#####2.减少原生和Java代码
- 移除不必要的代码生成

- 避免使用枚举

	枚举类型在编译时会生成类文件，占用空间。单个枚举在classes.dex中增加大约1 ~ 1.4kb的大小。当多个枚举时，会使apk包明显变大。

	建议采用@IntDef注解来替换或者接口替换。

- 减少原生二进制文件的大小
- 避免解压缩原生库

	在编译应用的发布版本时，您可以通过在应用清单的 <application> 元素中设置 android:extractNativeLibs="false"，将未压缩的 .so 文件打包在 APK 中。停用此标记可防止 PackageManager 在安装过程中将 .so 文件从 APK 复制到文件系统，并具有减小应用更新的额外好处。

- 由于目前市面CPU架构比较多，支持x86、x86_64、armeabi、armeabi-v7a、arm64-v8a、mips、mips64,前两种主要针对模拟器。
  
	实际上现在主流手机已经是armeabi、armeabi-v7a、arm64-v8a。

	其中：armeabi-v7a架构cpu可以支持armeabi，arm64-v8a可以支持armeabi-v7a和armeabi所需要的指令集，但速度上会逐次递减。
	
	mips64架构cpu可支持mips架构，速度同理逐次递减。
	
	由于考虑到各种架构的手机市场占有率及Apk包大小，在打包时可以酌情过滤掉部分ABI，过滤方式如下：
    

		android {
    		defaultConfig {
        		ndk {
        	    	abiFilters 'arm64-v8a', 'x86_64'
        		}
   			}
		}	


