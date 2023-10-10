### 前端开发常见问题

#### 一、antdv Cascader级联组件

##### 1.更改选择后的展示内容

参数：`displayRender`

```javascript
<a-cascader v-else
    :field-names="{ label: 'name', value: 'id', children: 'children' }"
    :options="gradeClassList"
    :display-render="displayRender"
    @change="changeGradeClass"
    placeholder="请选择班级"  />


//js代码
/**
 * 用于级联组件仅展示最后一级内容
 */
displayRender({ labels }){
  return labels[labels.length - 1];
},
```

##### 2.动态加载数据设置默认值

注意要使用`v-model`，不能使用`defaultValue`

注意要使用`v-model`，不能使用`defaultValue`

注意要使用`v-model`，不能使用`defaultValue`

静态数据使用defaultValue没问题，但是动态加载的数据就不能这么用了。

笔者是一个vue小白，就在这里掉进坑里了，折腾了老半天没爬上岸，最后没办法请大佬救场，分分钟给解决。

```javascript
<a-cascader v-else
   :field-names="{ label: 'name', value: 'id', children: 'children' }"
   :options="gradeClassList"
   v-model="gradeClassName"
   :display-render="displayRender"
   expandTrigger="hover"
   @change="changeGradeClass"
   placeholder="请选择班级"  />


/**
* 级联切换默认显示值
*/
gradeClassName(){
  let {gradeId, classId} = this.checkData || {}
  if (gradeId && classId)
    return [gradeId, classId]
  return []
}
```

注意：v-model值不能直接使用`['xx','xx']`，需要通过`变量`的方式，否则vs编辑器报错。

#### 二、Vue移动端弹窗滚动穿透

现象：

- 弹窗内容滑动到底部，再向上滑动弹窗底部内容跟随滑动；

- 弹窗内容滑动到顶部，再向下滑动弹窗底部内容跟随滑动；

解决办法：

在弹窗显示时，设置body的style的overflow属性值为hidden，弹窗关闭时恢复原来设置；

```javascript
//解决弹窗遮罩滚动问题
toggleShadowIosScroll(visible) {
	document.body.style.overflow = visible ? 'hidden' : 'scroll';
},
```

若未生效，可再对id为app的div标签的style增加overflow设置，如下：

```javascript
document.getElementById('app').style.overflow = visible ? 'hidden' : 'scroll'
```


