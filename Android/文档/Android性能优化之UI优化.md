[Android性能优化 - UI篇](https://www.jianshu.com/p/50b48f45e8ab)

[Android性能优化 - CPU/GPU篇](https://www.jianshu.com/p/5303fa133a47)


### 一、UI层级优化 ###

借助工具：Hierarchy View UI层级查看器

位置：Android SDK > tools > monitor.bat

可优化点：层级、

使用条件：工具仅能用于AS自带的模拟器上，对于真机不支持，想要支持比较麻烦，若要支持可参考[解决HierarchyViewer不能连接真机的问题](https://blog.csdn.net/autumn_xl/article/details/40741835)

工具使用步骤:

1. 双击monitor.bat 启动DDMS
2. 弹出的界面右上角有下图标，切换到【Hierarchy View】,如下图：
   ![hierarchy_view_0.png](https://upload-images.jianshu.io/upload_images/13549630-3ced70eacd45a8c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 左侧窗口切换到【Windows】,然后选中你的APP进程，进行下图操作：

![image.png](https://upload-images.jianshu.io/upload_images/13549630-f1f0d4514ab8f602.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4.按上步骤操作后，会在右侧弹出UI层级视图,如图：

![image.png](https://upload-images.jianshu.io/upload_images/13549630-ed4f2287843377a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过上图中，我们可以滑动视图可检测UI层级，检查是否有多余层级

5.点击上图箭头指向位置，可展示对应布局处measure、layout、draw使用的时间，根据数据看是否要对UI进行优化，如下图显示各布局时间：
![image.png](https://upload-images.jianshu.io/upload_images/13549630-dfd6b1f60c5ab984.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

图中三个圆点分别代表measure、layout、draw。
绿色：代表耗时少，性能优，比viewTree中超过50%的都要快；
黄色：代表性能稍差，比viewTree中超过50%的都要慢，可进行优化，提升性能；
红色：代表在viewTree中性能最差，要考虑进行重点优化；

6.根据工具分析优化建议
- Measure红点：可能是布局中嵌套了RelativeLayout，或是嵌套了LinearLayout都是用了Weight属性。

- layout红点：可能是布局层级太深

- draw红点：可能是自定义View绘制有问题，比如有复杂的计算等


###二、Lint 代码检测器
功能：检查代码中的可优化项

位置：打开AndroidStudio  点击菜单 > 【Analyze】 > 【Inspect Code】或者选中项目 > 【右键】> 【Analyze】 > 【Inspect Code】
 
也可单独对res目录进行分析，Lint工具会分析出布局中可优化项。如下图：
![image.png](https://upload-images.jianshu.io/upload_images/13549630-f8fd5f8ccaaae95f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

图中的XML中是我们在做UI优化时需要关注的。
- Deprecated API usage in XML  
过时的api属性引用，如：AbsoluteLayout。
- Unused XML schema declaration
未使用到的架构声明，主要体现在：未使用的命名空间；
![image.png](https://upload-images.jianshu.io/upload_images/13549630-2351eb4ce8070d65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- XML tag empty body
xml标签空的body，如：
  ```
  <declare-styleable name="indicator"></declare-styleable>
  <item android:color="@color/mBlueDark" android:state_pressed="true"></item>
  ```
  像上面这种空body的，建议修改成以下样式：
   ```
  <declare-styleable name="indicator"/>
  <item android:color="@color/mBlueDark" android:state_pressed="true"/>
  ```
- 无效属性。
比如：在RelativeLayout中使用android:weight属性。

### 三、UI布局中常见优化点 ###

#####1. UI布局的层级
没有使用的父布局（没有设置背景或大小限制，即没有特殊效果，仅用于控制子view），针对这种的父布局，则可以移除。尤其对通过<include>引入的布局通常都会带有一个父布局，此时要多注意了，若可去除，则可以采用<merge>替代。
例子：
parent.xml
```
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/color_bg_light_gray">
  <include layout="@layout/child"/>
</android.support.constraint.ConstraintLayout>
```
child.xml
```
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:id="@+id/tv_report_title"
        android:layout_width="wrap_content"
        android:layout_height="90px"
        android:gravity="center_vertical"
        android:layout_marginStart="40px"
        android:textSize="30px"
        android:textColor="#222222"
        android:textStyle="bold"
        tools:text="@string/str_radar_title"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>
</android.support.constraint.ConstraintLayout>
```
像这种的<include>引用就可以把child.xml中的根节点使用merge替换，修改后如下：
```
<merge xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:parentTag="android.support.constraint.ConstraintLayout">
    <TextView
        android:id="@+id/tv_report_title"
        android:layout_width="wrap_content"
        android:layout_height="90px"
        android:gravity="center_vertical"
        android:layout_marginStart="40px"
        android:textSize="30px"
        android:textColor="#222222"
        android:textStyle="bold"
        tools:text="@string/str_radar_title"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"/>
</merge >
```
```注：tools:parentTag="android.support.constraint.ConstraintLayout" 设置父标签，方便在UI布局中查看显示效果，很不错的小窍门```
使用参考文档：[include和merge使用](https://developer.android.google.cn/training/improving-layouts/reusing-layouts)

#####2. 选择合适的Layout
在层级相同时，在选择LinearLayout和RelativeLayout时，建议使用LinearLayout替代，因为RelativeLayout需要计算上下左右View去确定位置。

#####3. 善用layout及View的属性
在使用LinearLayout时，不要使用android:weight属性，若非要使用，建议使用ConstrainLayout替换LinearLayout。

#####4. 强烈推荐ConstraintLayout约束布局
该布局类似RelativeLayout，但功能更强大，可以设置百分比，约束view位置，可以设置group,批量设置group中的view的显示和隐藏等。
使用参考文档[ConstraintLayout](https://developer.android.google.cn/training/constraint-layout)

#####5. 考虑<ViewStub>标签
对于不长用的UI设置成GONE时，要考虑使用<ViewStub>替换，因为该标签引入的Layout不会被加载到内存，更不会被绘制；
```
<ViewStub
        android:id="@+id/stub_import"
        android:inflatedId="@+id/panel_import"
        android:layout="@layout/progress_overlay"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom" />
```
ViewStub使用请参考[视图加载延迟](https://developer.android.google.cn/training/improving-layouts/loading-ondemand)

#####6. 重复背景色
对于背景色相同的，可以去除多余的背景色，减少GPU的过渡绘制。
针对布局的重复背景色，可以留最上层一个即可，或者用其他方法替代。

#####7. 对于有select样式
对于select样式的，若normal情况下的颜色跟背景色一样，强烈建议将normal情况下背景色设置为透明色，减少GPU重绘。
举例：
```
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools = "http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    tools:parentTag="android.widget.LinearLayout"
    android:background="@color/color_left_subject_normal">
    <TextView 
      android:id="@+id/tv_left_subject_item"
      android:layout_width="match_parent"
      android:layout_height="90px"
      android:gravity="center"
      android:textAlignment="center"
      android:background="@drawable/btn_check_gray_to_black_bg"
      android:textColor="@color/white"
      android:textSize="24px"
      tools:text="学科"/>
</android.support.constraint.ConstraintLayout>
```
btn_check_gray_to_black_bg.xml代码如下：
```
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true" android:drawable="@color/color_left_subject_selected"/>
    <item android:state_selected="false" android:drawable="@color/transparent"/>
    <item android:drawable="@color/transparent"/>
</selector>
```
由于normal状态下背景色与父Layout背景色相同，所以TextView的选择样式中，normal状态可设置为transparent。

#####8.删除未使用的命名空间
处理方式：删除，参考Lint检查XML优化项。

#####9.空body情况
处理方式：修改成不带body结束标记，参考Lint检查XML优化项。

#####10.删除无效属性
处理方式：删除，参考Lint检查XML优化项。

#####11.XML布局文件中的字符串、View尺寸、字体大小、颜色定义到values中
- 字符串 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;定义在strings.xml中
- view尺寸 &nbsp;&nbsp;&nbsp;&nbsp;定义在dimens.xml
- 字体大小 &nbsp;&nbsp;&nbsp;&nbsp;定义在dimens.xml
- 颜色 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;定义在colors.xml中

优点：
- 可重复使用
- 修改方便，不用到处查找xml文件
- 便于屏幕适配
- 便于多语言化

#####12.避免使用alpha属性
原因：谨慎使用alpha，会对性能有一定影响，因为如果后渲染的元素带有alpha值，这个元素会和屏幕上已渲染好的元素做blend处理。
替代方案：通过设置颜色的透明的来代替。
```
<View
        android:layout_width="match_parent"
        android:layout_height="1px"
        android:alpha="0.5"
        android:background="#ff0000"/>
```
可通过下方式替换：
```
<View
        android:layout_width="match_parent"
        android:layout_height="1px"
        android:background="#80ff0000"/>
```

#####13.尽量少用wrap_content
针对能固定尺寸的尽量用固定的大小设置View的尺寸，这样可以减少onMeasure次数，提高效率。


#####14.自定义View
- 在自定义view中 onMeasure onLayout onDraw方法中不要做耗时的计算；
- 在onDraw方法中减少过度绘制Over DrawCall，比如：绘制重叠的图片时可以采用clipRect方法减少GPU的过度绘制;
自定义View优化会在后续CPU和GPU性能优化中会详细讲解。



**暂时就总结这些，以后碰到再补充。如有遗漏，欢迎留言！**

