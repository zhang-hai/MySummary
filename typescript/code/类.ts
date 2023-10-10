class User{
    name:string
    age:number

    constructor(name:string,age:number){
        this.name = name
        this.age = age
    }

    toString(){
        console.log("xxxx")
    }
}
//类实例化
let user = new User('zhang',10)
//使用
console.log(user.name)
console.log(user.age)
