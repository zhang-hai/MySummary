//定义一个父类
class Shape{
    protected width:number
    height:number
    constructor(w:number,h:number){
        this.width = w
        this.height = h
    }
}
//继承Shape父类
class Line extends Shape{
    private color:string
    readonly bold:number = 2

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

let obj :{readonly age:number,name:string}= {age:20,name:'zhang'}


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