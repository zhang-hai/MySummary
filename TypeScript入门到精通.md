### TypeScript入门到精通

##### 1.TypeScript介绍

###### 1.1 TypeScript是什么

TypeScript，简称为TS,是javascript的超集,js有的功能ts都有。

TypeScript = Type + javascript，即在js的基础上增加了类型支持。

TypeScript是由微软开发的开源编程语言，可以在任何运行js的地方运行。

###### 1.2 TypeScript为什么要为js添加类型支持

写过JS代码的同学都值得，JS是一个弱类型脚本语言，对使用的数据类型未做严格的要求，可以进行类型转换，简单又灵活。但是正因为这一特点，经常出现类型类型错误。为了解决这一问题，因此产生了TypeScript。

TypeScript和JavaScript对比：

| 语言         | 编程语言动静 | 代码检查时期 |
| ---------- | ------ | ------ |
| TypeScript | 静态类型   | 编译期    |
| JavaScript | 动态类型   | 执行期    |

###### 1.3 相比JS的优势

1.更早的发现代码错误，减少bug数量，提示效率；

2.配合编译工具，有很好的代码提示，增强开发体验；

3.有强大的类型系统提升代码的可维护性；

4.有类型推断机制，不需要在代码的每个地方都显示设置类型；

另外，目前一些框架源码都默认支持TS，如：Vue3源码使用TS重写、Angular默认支持TS、uniapp和微信小程序也均支持TS开发，可见TS已经成为前端项目的首选编程语言。

##### 2.TypeScript初体验

**安装TypeScript工具**

命令：`npm i -g typescript`

浏览器/node.js无法直接运行ts文件，需要编译成js再运行

编译运行命令

tsc xxx.ts

node xxx.js

**简化编译运行操作**

可通过`ts-node`简化编译运行命令

先全局安装`ts-node`：`npm i -g ts-node`

安装完成后，直接通过命令`ts-node xxx.ts`，实现编译运行。

注意：该命令不会直接生成js文件。

##### 3.TypeScript常用类型

###### 3.1 类型注解

示例：

```typescript
let age:number = 31
```

说明：代码中的:number就是类型注解。

作用：为变量增加类型约束，表示该变量只能是这个类型，不能用其它类型的值赋值给它，否则报错。

###### 3.2 常用基础类型

TS中的常用基础类型可以细分为两类：

- JS已有类型
  
  基本类型：number/string/boolean/null/undefined/symbol(es6新增)
  
  对象类型：object（包括：数组、对象、函数等）

- TS新增类型
  
  联合类型、自定义类型（类型别名）、接口、元祖、字面量类型、枚举、void、any等。

###### 3.3 基本类型

number/string/boolean/null/undefined/symbol(es6新增)

用法与Js一致，示例：

```typescript
let age:number = 10
let name:string = '张三'
let isStudent:boolean = false
let ss:null  =null
let abc:undefined = undefined
let dd:symbol = Symbol()
```

###### 3.4 数组类型

示例：

```typescript
let ages:number[] = [1,2,3]    //推荐该方式写法
let ages2:Array<number> = [1,2,3]
```

扩展：如果数组中是否可以有多个类型呢？

答案是肯定的，这时可以采用联合类型。

###### 3.5 联合类型

通过`(xx | xx)`方式，如下示例：

```typescript
let ages:(number | string)[] = [1,2,'a']
```

`注：一定要带小括号，若不带小括号则表示该变量要么是number类型要么是string[]类型。`

###### 3.6 类型别名

声明：type 别名 = 实际类型

使用场景：当同一类型复杂但又被多次使用时，可以通过类型别名，简化该类型。

关键字：`type`

示例：

```typescript
type Num = number
let age:num = 123


type CusArray = (number|boolean)[]
let arr:CusArray = [1,false]
```

###### 3.7 函数类型

指给函数指定`参数类型`和`返回值类型`

示例：

```typescript
//方式一：函数声明
function sub(num1:number,num2:number):number{
    return num1 - num2
}
//方式二：函数表达式
const sub = (num1:number,num2:number):number =>{
    return num1 - num2
}
```

当采用<mark>函数表达式形式</mark>定义函数时还可采用`类似给变量指定类型的方式`同时指定参数类型、返回值类型,如下示例：

```typescript
const sub:(num1:number,num2:number):number = (num1,num2)=>{
    return num1 - num2
}
```

<mark>注意：该方式仅适用函数表达式形式</mark>

*可选参数*

定义：在函数的参数名称后面增加一个`?`

特点：可选参数必须放在函数参数的后面，不能后面跟随必传参数。

示例：

```typescript
function sub(n1:number,n2:number,ret?:number){
    return n1 - n2
}
```

###### 3.8 对象类型

定义：用大括号给属性指定类型，有多个属性 时用`;`隔开。

如下示例

```typescript
let person:{name:string;age:number;toString():void} = {
    name:'张三',
    age:10,
    toString(){
        console.log('name:'+name+',age:'+age)
    }
}
```

<mark>属性还可以采用多行的形式，这时`;`可省略</mark>，如下写法：

```typescript
let person:{
    name:string
    age:number
    toString():void
} = {
    name:'张三',
    age:10,
    toString(){
        console.log('name:'+name+',age:'+age)
    }
}
```

可选属性

函数存在可选变量，对象的属性也存在可选属性，定义方式也是采用关键字`?`

```typescript
function output(data:{tag:string;msg?:string}){
    console.log(data.tag+data.msg)
}
```

###### 3.9 接口

定义：采用关键字`interface`，形式：interface xxx{}.

```typescript
//声明接口
interface IUser{
    name:string
    age:number
    toString():void
}

//使用接口
let user:IUser={
    name:'张三',
    age:20,
    toString(){
        console.log('xxx')
    }
}
```

**对比**：接口（interface）和类型别名（type）区别？

- 相同点：都可以给对象指定类型。

- 不同点：
  
  - 接口，仅为对象指定类型
  
  - 类型别名，可以为任意类型指定别名，范围更广

**继承特性**

当两个或多个接口有相同的属性或函数，可以将公共部分单独抽离出来，通过继承方式来实现复用。

关键字：**`extends`**

如下示例：

```typescript
interface IPoint{
    x:number
    y:number
}
//ILine 拥有了x,y属性
interface ILine extends IPoint{
    width:number
}
//ICircle 拥有了x,y属性
interface ICircle extends IPoint{
    radius:number
}
```

###### 3.10 元组类型

定义：是另一种类型的数组，它明确了元素个数和对应索引的类型。

```typescript
let color:[number,number,number] = [255,255,255]
```

###### 3.11 类型推论

TS中，某些没有明确指定类型的地方，TS可以帮助我们提供类型。所以由于存在类型推论机制存在，在一些场景类型注解是可以省略不写的。

那么什么场景下TS可以对类型进行推论呢？

1.声明变量时并初始化（即赋值情况）

```typescript
//声明变量并初始化时，可以省略类型注解
let age = 10
```

2.函数返回值类型明确的时

```typescript
//函数返回值的类型可以省略
function sub(num1:number,num2:number){
    return num1 - num2
}
```

###### 3.12 类型断言

使用场景：调用函数时，其返回值不是具体的类型。

定义：关键字`as`，说白了就是**类型强制转换**

形式：<mark>as [具体类型]</mark>

```typescript
//常用 as 
const link = document.getElementById('link') as HTMLAnchorElement
//不推荐写法
const link = <HTMLAnchorElement>document.getElementById('link')
```

###### 3.13 字面量类型

定义：采用某些特点的值作为变量的类型的方式即为字面量类型。

```typescript
// 普通变量 num的类型为number
let num:number = 10

// 常量num1的类型为8，而不是number类型了
const num1 = 8
```

字面量类型不仅仅适用于number类型，对其它类型同样适用。

适用场景：往往会配合联合类型一起使用，实现一组明确的可选值列表，类似枚举。

```typescript
//表示参数shape只能是line/circle/rectangle/triangle中的一个值
function createShape(shape:'line' | 'circle' | 'rectangle' | 'triangle'){
    ....
}
```

###### 3.14 枚举

定义：定义一组命名常量，描述一个值，该值可以是这些命名常量中一个。

关键字：`enum`

说明：功能类似字面量类型+联合类型组合。

```typescript
//定义枚举
enum Shape{ 
    Line,Circle,Rectangle,Triangle
}

//使用
function createShape(shape:Shape){
    console.log("shape:"+shape)
}

//调用上面函数
createShape(Shape.Line)
```

注意：`枚举成员是有值的`，默认为：从0开始自增的数值。

**`数字枚举`**：当枚举成员的值为数字

当然也可以给枚举成员初始化值，如下：

```typescript
//此时值为：Line->3,Circle->4,Rectangle->5,Triangle->6
enum Shape{Line = 3,Circle,Rectangle,Triangle}

//同样可以给每个成员都设置值
enum Shape{Line = 3,Circle=5,Rectangle=8,Triangle=9}
```

**`字符串枚举`**：枚举的成员值为字符串，并且**每个成员均需要初始化**

```typescript
enum Shape{
    Line = 'line',
    Circle = 'circle',
    Rectangle = 'rectangle',
    Triangle = 'triangle'
}
```

值得注意的是：字符串枚举是没有自增长行为的。

上述字符串枚举被`tsc`命令编译成如下js代码：

```javascript
var Shape;
(function (Shape) {
    Shape["Line"] = "line";
    Shape["Circle"] = "circle";
    Shape["Rectangle"] = "rectangle";
    Shape["Triangle"] = "triangle";
})(Shape || (Shape = {}));
```

一般情况下，推荐使用字面量类型+联合类型组合的方式，相比枚举来说会更简洁、直观、高效。

###### 3.15 any类型

原则：<mark>不推荐使用any</mark>，这会让TypeScript变成'AnyScript'，会失去TypeScript的优势。

当使用Any类型时，可以对该对象进行任意操作，并且不会有相关的代码信息提示，包括可能存在的错误。

```typescript
let obj:any = {a:2}
//以下操作均不会有代码信息提示，包括可能存在的错误信息
obj.y = 10
obj()
```

注意下两种情况会默认为any类型

- 当定义一个变量未设置类型注解并且未初始化值时

- 函数参数不加类型

```typescript
//这种定义时，obj的类型即为any类型
let obj

//这这种定义，num1 num2即为any类型
function sub(num1,num2){
  ...  
}
```

###### 3.16 typeof类型

 `typeof`提供数据类型查询功能，在TS中可以用来查询上下文中<mark>变量或属性</mark>的类型。

```typescript
let point= {x:1,y:2}

//这种方式表示p可以引用变量point的类型，即通过typeof查询point的类型
function formatPoint(p:typeof point){

}
```

##### 4.TypeScript高级类型

###### 4.1 类

定义：采用关键字 `class`

形式：class 类名{}

```typescript
class User{
    name:string
    age:number
}
```

给类添加构造函数，构造函数名为`constructor`

```typescript
class User{
    name:string
    age:number

    constructor(name:string,age:number){
        this.name = name
        this.age = age
    }
}
```

值得注意：<mark>构造函数不能设置返回值</mark>

类通过关键字`new`进行实例化

```typescript
//类实例化
let user = new User('zhang',10)
//使用
console.log(user.name)
console.log(user.age)
```

**类继承**

两种继承方式

- 类型接口类型，继承同样采用关键字`extends`，继承后具备父类的属性和方法。

示例：

```typescript
//定义一个父类
class Shape{
    width:number
    height:number
    constructor(w:number,h:number){
        this.width = w
        this.height = h
    }
}
//继承Shape父类
class Line extends Shape{

}
//实例化，Line类具备了父类的属性和方法
let line = new Line(10,2)
```

- 采用关键字`implements`实现接口

```typescript
//定义一个接口
interface IShape{
    name:string
    toString():void
}
//实现IShape接口
class Squre implements IShape{
    name: string

    //示例父类接口
    toString(): void {

    }
}
```

注意：该方式下子类必须实现接口中指定的所有方法和属性

**类成员的可见性**

也可以理解为属性和方法的作用域范围。

修饰词：`public(公有的)`、`protected(受保护的)`、`private(私有的)`。

使用范围进一步说明：

- public：公有成员，在所有地方都可访问，<mark>类属性和方法默认public</mark>；

- protected：仅在当前类和其子类中可见，<mark>对其实例对象不可见</mark>

- private：仅在声明类内部可见；

如下示例：

```typescript
//定义一个父类
class Shape{
    //这个属性是受保护的
    protected width:number
    height:number
    constructor(w:number,h:number){
        this.width = w
        this.height = h
    }
}
//继承Shape父类
class Line extends Shape{
    //这个属性是私有属性
    private color:string

    toString(){
        //color仅在声明类内部可见  with对声明类和子类可见
        console.log(`color:${this.color},width:${this.width},height:${this.height}`)
    }
}
//实例化，Line类具备了父类的属性和方法
let line = new Line(10,2)
//访问不到private属性color，报错
line.color
//访问不到protect属性width，报错
line.width
//能正常访问public属性height
line.height
```

`readonly(只读修饰符)`

readonly：只读修饰符，<mark>仅用于修饰属性</mark>,只读属性的默认访问范围是public

如：readonly bold :number = 2

使用readonly时建议添加类型，否则变为字面量类型。

另外不仅限于在类属性中使用，在接口属性、对象类型中也可以使用。

```typescript
//接口中使用
interface IUser{
    readonly name:string
}
//对象类型中使用
let obj :{readonly age:number,name:string}= {age:20,name:'zhang'}
//报错：修改age属性值
obj.age = 11
```
