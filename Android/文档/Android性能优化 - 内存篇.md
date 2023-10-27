[Android性能优化 - UI篇](https://www.jianshu.com/p/50b48f45e8ab)

[Android性能优化 - CPU/GPU篇](https://www.jianshu.com/p/5303fa133a47)


###一、Android GC机制简介

在Android中，通过new的对象都会分配到堆内存中，堆内存有分为两大块：永久空间和堆空间。
- 永久即持久代（Permanent Generation），主要存放的是Java类定义信息，与垃圾收集器要收集的Java对象关系不大。
- Heap = {Old + NEW = {Eden，from，to}}，Old即年老代（Old Generation），New即年轻代（Young Generation）。年老代和年轻代的划分对垃圾收集影响比较大。

![](https://upload-images.jianshu.io/upload_images/13549630-16736a9eef45aa7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######年轻代
年轻代中分配比例大约为：Eden占8/10，from和to各占1/10。
内存分配及GC流程如下：
1.新创建的对象都会分配到Eden区；
2.当触发GC时会回收掉Eden区的对象，幸存的对象会被复制到From区，新创建的对象继续放到Eden区。
3.再次触发GC时会回收掉Eden区和From区的对象，再有幸存对象时，则全部复制到to区，继续步骤1，新建对象；
4.等到Eden区分配满，再次触发GC时，会回收掉Eden区和to区的对象，最后把幸存的对象全部复制到from区，然后继续执行步骤1；
5.如此循环往复，每次GC都会把Eden区和from或者to中的对象进行回收，并全部复制到from或to中空的那个中，每次有幸存者时计数增加1,当幸存者的技术累计到一定数量时，仍未被回收，则该对象被则被复制到老年代区；

针对年轻代的垃圾回收即Young GC。

######老年代

在年轻代中经历了Ñ次（可配置）垃圾回收后仍然存活的对象，就会被复制到年老代中。因此，可以认为年老代中存放的都是一些生命周期较长的对象。

针对年老代的垃圾回收即Full GC。

在完全GC后，若Survivor区及年老代仍然无法存放从Eden复制过来的对象，则会导致JVM无法在Eden区为新生成的对象申请内存，即出现“内存不足”。

######OOM

OOM（“Out of Memory”）异常一般主要有如下2种原因：

1.年老代溢出，表现为：java.lang.OutOfMemoryError：Javaheapspace
这是最常见的情况，产生的原因可能是：内存泄漏、内存碎片等原因。
这种方式的OOM是我们本文的重点。

2.持久代溢出，表现为：java.lang.OutOfMemoryError：PermGenspace


###二、辅助监测工具

#####1.Android Monitor中DDMS下的Heap Dump

Android Device Monitor工具在Android SDK目录下的tools中，点击直接运行，即可。

![image.png](https://upload-images.jianshu.io/upload_images/13549630-0e339dc1180d11ae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中总览视图可以查看整体的内存情况，表中的显示信息如下所示：

- Heap Size 堆栈分配给该应用程序的内存大小
- Allocated 已使用的内存大小
- Free 空闲的内存大小
- %Used 当前Heap的使用率（Allocated/Heap Size）
- Objects 对象的数量

Heap Dump检测内存泄漏：通常做法是使用Update Heap进行内存监听，然后操作可能发生泄漏的APP功能、界面，并点击Cause GC进行手动GC，经过多次操作后查看data object的Total Size大小是否有很大的变化，如果有则可能发生了内存泄漏，导致内存使用不断增大。

#####2.Android Monitor中DDMS下的Allocation Tracker

使用Heap Dump可以让你对APP的内存整体使用情况进行掌控，但缺点是无法了解每块内存具体分配给哪个对象了，这时就需要使用Allocation Tracker工具来进行内存跟踪。它允许你在执行某些操作的同时监视在何处分配对象，了解这些分配使你能够调整与这些操作相关的方法调用，以优化应用程序性能和内存使用。

Allocation Tracker能够做到如下的事情：

- 显示代码分配对象类型、大小、分配线程和堆栈跟踪的时间和位置。
- 通过重复的分配/释放模式帮助识别内存变化。
- 当与 HPROF Viewer结合使用时，可以帮助你跟踪内存泄漏。例如，如果你在堆上看到一个bitmap对象，你可以使用Allocation Tracker来找到其分配的位置。


#####3.MAT

想要深入的进行分析并确定内存泄漏，就要分析疑似发生内存泄漏时所生成堆存储文件。堆存储文件可以使用DDMS或者Memory Monitor来生成，输出的文件格式为hprof，然后使用MAT来分析堆存储文件。

MAT,全称为Memory Analysis Tool，是对内存进行详细分析的工具，它是Eclipse的插件，如果用Android Studio进行开发则需要单独下载它，可独立运行。[下载地址](http://eclipse.org/mat/)

#####4.LeakCanary库
LeakCanary库是github上优秀的第三方开源库，通过该库可以监控内存是否有泄漏。其原理是利用对象引用可达性分析算法来进行检测的，当出现内存泄漏时会在通知栏中进行通知。
使用方式不过多介绍，请参考[LeakCanary库](https://github.com/square/leakcanary)

#####5.Android studio自带的Profiler工具

启动Andrroid studio，连接手机或模拟器，点击下按钮，启动要监控的应用

![](https://upload-images.jianshu.io/upload_images/13549630-1f507a7a92a2c016.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

等应用启动后，在as底部会启动profiler分析器，点击Memory行会进入到Memory使用详情界面。

![](https://upload-images.jianshu.io/upload_images/13549630-dd9fff12a8336bc9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

等采集完数据后，AS会自动分析Heap Dump的数据，如下图

![](https://upload-images.jianshu.io/upload_images/13549630-625b0bb6c284b73a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](https://upload-images.jianshu.io/upload_images/13549630-358fbfa0dd9b0776.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

图中筛选项说明
 - app heap 指当前App使用的heap
- image heap 指磁盘上当前App的内存映射拷贝
- zygote heap zygote进程Heap（fragment占用的Heap）

我们筛选时一般按app heap进行筛选，只需要看我们自己的app堆内存分配情况。

![](https://upload-images.jianshu.io/upload_images/13549630-b509d302972a2159.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

各列信息说明
- Package Name  包名
- Allocations 分配数
- Native Size Native的大小
- Shallow Size  对象本身占用内存的大小，不包含对其他对象的引用，也就是对象头加成员变量（不是成员变量的值）的总和
- Retained Size 对象自己的shallow size，加上从该对象能直接或间接访问到对象的shallow size之和。即该类的所有对象可支配的内存大小

![](https://upload-images.jianshu.io/upload_images/13549630-a4a2216ef1065b6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

说明：
Instance View 窗口是在Heap dump窗口中选择一个类展示出来的，该窗口展示了所有相关的实例对象。
点击任意一个实例对象，就会在下部展示出该对象的所有引用链，可通过```Depth（深度）列```依次查看对象的引用链，选中一个，右键可以弹出【jump to source】和 【Go to Instance】，点击可跳到引用的代码中，这样很容易查出是否有泄漏问题。

![](https://upload-images.jianshu.io/upload_images/13549630-6b0209fde915660d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



> 针对1、2、3工具使用可参考：[Android 内存检测工具](https://blog.csdn.net/huaxun66/article/details/77650909)


###三、常见内存问题

#####1.内存泄漏
文章开头也说明了内存gc机制，所谓内存泄漏（Memory Leak）是指程序中己动态分配的堆内存由于某种原因程序未释放或无法释放，gc时一直不能被回收，造成系统内存的浪费，导致程序运行速度减慢甚至系统崩溃等严重后果。

######表现

app占用内存高居不下，即使Activity被销毁或APP退出时内存仅小幅度降低，再次进入Activity时占用内存比之前销毁时还要高。
内存泄漏中常见例子：如handler、popwindow等，下面就已Handler为例。

```
public class MyActivity extends Activity{
  private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg){
            Log.i("MyActivity","Test Memory Leak.");
            handler.sendEmptyMessageDelayed(100,10000);
        }
  };

  @Override
  public void onCreate(@Nullable Bundle savedInstanceState){
      //延迟10s发送一个空的消息
      handler.sendEmptyMessageDelayed(100,10000);
  }
}
```
此时如果，调用finish()方法结束Activity，则会发现Activity的对象一直被持有，无法被gc回收。

![](https://upload-images.jianshu.io/upload_images/13549630-71cce284180ed694.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过查看发现存在对象引用链发现有message持有Activity的context对象造成无法被回收，引起内存泄漏。
优化，``` 重新Activity的onDestroy方法，添加handler.removeCallbacksAndMessages(null); ``` message消息从队列中移除，这样就可以被回收了，下图是优化后的效果：

![](https://upload-images.jianshu.io/upload_images/13549630-8c4cd513438eda53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此时会发现在对应的包下面不存在我们的app的包名，说明Activity占用的内存已经被gc回收。


#####2.内存抖动

App在使用过程中内存数据高低波动明显，或者界面停止不动（无任何操作）内存在不断增加、降低、再增加、再降低如此循环。
同样，举个例子简单辅助说明下：
```
public void click(View view) {
        int id = view.getId();
        if(id == R.id.btn_more_fragments){
            //startActivity(new Intent(this,RadarChartActivity.class));
            handler.sendEmptyMessageDelayed(100,1000);
        }
    }

    private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            for (int i = 0;i< 100;i++){
                byte[] b = new byte[2048];
            }
            handler.sendEmptyMessageDelayed(100,100);
        }
    };
```
运行后观察内存，如下图

![](https://upload-images.jianshu.io/upload_images/13549630-dfbaf05d552c208d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

优化方法``` 采用内存复用方式 ```将byte[] b放到循环外面作为Activity的成员变量中，优化代码如下：
```
//放到全局
private byte[] b;
...
 for (int i = 0;i< 100;i++){
         b = new byte[2048];
 }
```

![](https://upload-images.jianshu.io/upload_images/13549630-777c5f81ee1e2177.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对操作大数据时，如Bitmap尽量做到内存复用，而不是频繁的new对象去分配内存空间。

#####3.内存碎片
内存碎片指在堆内存中存在小块的内存空间，始终得不到利用，从而造成内存空间浪费。

![](https://upload-images.jianshu.io/upload_images/13549630-b2a73382c305dc3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4KB来为内存分页中每一页的大小。

通过使用Android support V4中提供的Pools对象池，可以很好的解决内存碎片问题。



###四、常见内存效率更高的代码结构

待后续补充...