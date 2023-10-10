enum Shape{
    Line = 'line',
    Circle = 'circle',
    Rectangle = 'rectangle',
    Triangle = 'triangle'
}


//使用
function createShape(shape:Shape){
    console.log("shape:"+shape)
}

//调用上面函数
createShape(Shape.Line)