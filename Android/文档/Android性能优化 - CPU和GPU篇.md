[Android性能优化 - UI篇](https://www.jianshu.com/p/50b48f45e8ab)

[Android性能优化 - CPU/GPU篇](https://www.jianshu.com/p/5303fa133a47)

####前言
本篇主要讲解APP性能优化路上关于CPU、GPU的优化。先来了解下这两个的主要功能：

CPU：叫中央处理器，作为计算机系统的<font color=red>运算和控制核心</font>，是信息处理、程序运行的最终执行单元。

GPU: 叫图形处理器，是一种专门在个人电脑、工作站、游戏机和一些移动设备（如平板电脑、智能手机等）上做图像和图形相关运算工作的微处理器。

通过对CPU和GPU简单的了解可以知道，CPU主要用于计算，GPU主要用户UI绘制。

了解了这些后，下面我们就进入正题。

####一、优化CPU、GPU的优点

在讲如何优化前，我们先分析下为何要进行优化，给我们的APP带来哪些好处。

 - 优化CPU,减少CPU计算工作，缩短了计算消耗的时间，提高计算效率；
 - 优化GPU，可以减少GPU的UI绘制工作，提升绘制效率；
 - 减少电耗，CPU计算量少了，GPU绘制少了，对手机电量损耗就少；
 - 减少手机发热，电量损耗减少，产生的热量自然就少了；
 - 减少APP UI卡顿，CPU和GPU效率提高了，就能更好的保证屏幕刷新在16ms（为啥？后面会讲到）内完成；
 - app更流畅，提升用户体验；
 
等等，还有其他的好处，这里讲了比较重要的几点。

既然有那么多好处，那么我们讲讲如何做吧。


![timg.jpg](https://upload-images.jianshu.io/upload_images/13549630-d0d6e9c6c16c91ec.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####二、简介屏幕刷新机制

屏幕的刷新过程是每一行从左到右（行刷新，水平刷新，Horizontal Scanning），从上到下（屏幕刷新，垂直刷新，Vertical Scanning）。当整个屏幕刷新完毕，即一个垂直刷新周期完成，会有短暂的空白期，此时发出 VSync 信号。所以，VSync 中的 V 指的是垂直刷新中的垂直-Vertical。

Android系统每隔16ms（1s/60fps计算结果）发出VSYNC信号，触发对UI进行渲染，如果每次渲染都成功，这样就能够达到流畅的画面所需要的60fps，为了能够实现60fps，这意味着用户的大多数操作都必须在16ms内完成；但是如果主线程执行一些太耗时操作或短时间内执行太多任务，周期超过16ms，就会导致丢帧，丢帧后，UI刷新只能等到下一次VSYNC信号到来时在绘制，因此32ms内看到的是同一帧。

丢帧情况：

![image](https://upload-images.jianshu.io/upload_images/13549630-c41c3c24767bc439.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上图：可见第二次vsync到来需要显示内容时，CPU和GPU还没有来得及准备好下一帧的数据，所以只能接着显示上一帧的数据。

正常情况，非丢帧图：

![image](https://upload-images.jianshu.io/upload_images/13549630-0deb4915501821ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

CPU/GPU接收vsync信号提前准备下一帧要显示的内容，所以能够及时准备好每一帧的数据，保证画面的流程。

> 参考自[Android 显示系统：Vsync机制](https://www.cnblogs.com/blogs-of-lxl/p/11443693.html)


####三、CPU优化

感觉叫CPU优化不太合理，说成APP在CPU方向上的优化可能更贴切些，反正先姑且这么说吧。

#####1.CPU过高引起的问题

- ANR，主线程响应超时，有耗时工作占用主线程超过5S;
- 手机发热，电量损耗过快；
- UI丢帧、卡顿，操作不流畅；
- APP响应慢等；

#####2.优化方向

- 减少主线程耗时工作；
- 减少主线程短时间内的执行的任务量，分散做；
- 少做、提前做、延迟做；
- 异步执行任务；
- 针对自定义View,切勿在onDraw中做大量计算工作；

#####3.介绍CPU优化的辅助工具

CPU分析工具有两种：Android Monitor 和CPU性能分析工具Trace Viewer。

在Android studio新版本讲两者合并统一到CPU Profiler 中，下面就以新版AS 3.6.2版本为例，讲解工具如何使用及如何分析CPU占用。

######1.整体分析APP中CPU消耗

首先点击【Profiler】按钮启动APP

![](https://upload-images.jianshu.io/upload_images/13549630-6b41a6a89457dcea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

启动后，会在AS下部显示如下窗口：

![](https://upload-images.jianshu.io/upload_images/13549630-b3c882df62082b77.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击红色区域，进入到显示CPU详情数据窗口界面，如图：

![](https://upload-images.jianshu.io/upload_images/13549630-5b9e4f923daab0af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


正常情况下仅能看到CPU使用图，具体的信息是看不到的。那么我们在某中情况下看到CPU使用过高，那么我们怎么看具体在哪里使用的呢？

点击【Record】按钮开始记录CPU使用数据，然后做你自己的操作，等看到你想要的CPU过高的那段数据后，点击【Stop】停止记录，稍等片刻工具就好自动分析记录的CPU数据，如下图：

![](https://upload-images.jianshu.io/upload_images/13549630-a911c6ffc216e487.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

找到我们自己的代码后，进行逐一排查就可以很容易定位问题和进行优化。

好了，工具使用介绍完了。
那么如果我只想对单个方法或一段代码进行分析CPU消耗怎么做呢？也很简单，两行代码搞定。

######2.使用Debug对单个方法或代码块进行CPU监控
很简单，使用Debug.startMethodTracing()和Debug.stopMethodTracing()两个方法。
场景：监控方法或代码块，在监控APP启动耗时尤为有用，因为APP启动使用Profiler是监控不到的。
如下例子：
```
public void showPublishTask(Activity activity){
        //开启记录trace数据
        //参数,为生成的trace文件名称，默认存储目录为：getExternalFilesDir，即默认目录为：Android/data/包名/files/
       //也可自己指定一个目录如：sdcard/myApp.trace
        Debug.startMethodTracing("myApp");
        
        CommonHttpModel.findCurTeachingSubjects(activity,null);
        mPopup = new PublishTaskPopup(activity);
        mPopup.setCallback((OnCommonListener<Boolean>) b -> mPopup = null);
        mPopup.showAtLocation(activity.getWindow().getDecorView(), Gravity.CENTER,0,0);
        
        //停止tracing
        Debug.stopMethodTracing();
    }
```
```注意：因涉及到向写入文件，故需要增加sdcard的读写权限，切记！切记！切记！```

允许APP，执行该段代码后，会在指定的目录下生成myApp.trace文件，将该文件导出在AS中打开即可进行分析，最终结果如下图：

![](https://upload-images.jianshu.io/upload_images/13549630-ffc6a556d77cbe64.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以上就是CPU辅助工具介绍，是不是很简单。
到此处CPU相关的优化就介绍完了。

![](https://upload-images.jianshu.io/upload_images/13549630-44d41fcd071ef660.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


####四、GPU优化
Android 包含一些设备上的开发者选项，可帮助您直观地查看您的应用可能会在何处遇到界面渲染问题，如执行不必要的渲染工作，或执行长时间的线程和 GPU 操作。

######开启GPU 过度绘制
----------
打开手机【设置】->【开发者模式】-> 找到【调试GPU过度绘制】点击，弹出【调试GPU过度绘制选择窗口】，选中【显示过度绘制区域】，整个手机屏幕上就会显示不同的颜色，打开我们自己的APP就可以进行检测排查了，

![](https://upload-images.jianshu.io/upload_images/13549630-19035f95be7ed4a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


不同的颜色代表过度绘制次数如下表

- 真彩色：没有过度绘制
- 蓝色：过度绘制 1 次
- 绿色：过度绘制 2 次
- 粉色：过度绘制 3 次
- 红色：过度绘制 4 次或更多次

从上图可以看到不同的过度绘制次数。
当碰到绿色以上的时候，就要考虑进行优化了。

######开启GPU分析器
-------------------
打开手机【设置】->【开发者模式】，在【监控】部分找到【GPU呈现模式分析】，点击后弹窗选择窗口，选中【在屏幕上显示为条形图】，这时候会看到屏幕上GPU绘制线条，如下图：

![](https://upload-images.jianshu.io/upload_images/13549630-20d5c99ae3d5ee0a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下面是有关上图的几点说明：
- 对于每个可见应用，该工具将显示一个图形。
- 沿水平轴的每个竖条代表一个帧，每个竖条的高度表示渲染该帧所花的时间（以毫秒为单位）。
- 水平绿线表示 16 毫秒。要实现每秒 60 帧，代表每个帧的竖条需要保持在此线以下。当竖条超出此线时，可能会使动画出现暂停。
- 该工具通过加宽对应的竖条并降低透明度来突出显示超出 16 毫秒阈值的帧。
- 每个竖条都有与渲染管道中某个阶段对应的彩色区段。区段数因设备的 API 级别不同而异。

以下为个颜色代表的含义：

4.0（API 级别 14）和 5.0（API 级别 21）之间的 Android 版本具有蓝色、紫色、红色和橙色区段。低于 4.0 的 Android 版本只有蓝色、红色和橙色区段。
下表显示的是 Android 4.0 和 5.0 中的竖条区段。

![](https://upload-images.jianshu.io/upload_images/13549630-e843400deb2d07f2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

下表介绍了使用运行 Android 6.0 及更高版本的设备时分析器输出中某个竖条的每个区段。

![](https://upload-images.jianshu.io/upload_images/13549630-55bf015ee7d1076f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 参考[检查 GPU 渲染速度和过度绘制](https://developer.android.google.cn/topic/performance/rendering/inspect-gpu-rendering)


#####GPU优化方法
---------------------------
1.减少过度绘制
  - 移除布局中不需要的背景，移除不必要的背景可以快速提高渲染性能。不必要的背景可能永远不可见，因为它会被应用在该视图上绘制的任何其他内容完全覆盖；
  - 使视图层次结构扁平化，减少view重叠的数量。
  - 降低透明度，在屏幕上渲染透明像素，即所谓的透明度渲染，是导致过度绘制的重要因素
  - 若View带点击特效，normal状态下与背景色相同时，可将normal状态的颜色设置为透明色；

2.减少Drawcall次数
  - 针对自定义的View，可使用clipRect减少DrawCall次数，比如绘制重叠的两个图片时，底图被覆盖的区域完全可以不用绘制，如下图：

![优化前](https://upload-images.jianshu.io/upload_images/13549630-44727e1ce0bf5d2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![优化后](https://upload-images.jianshu.io/upload_images/13549630-37974936ed6f1518.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> GPU的优化主要涉及到UI，可以参考[Android性能优化 - UI篇](https://www.jianshu.com/p/50b48f45e8ab)

