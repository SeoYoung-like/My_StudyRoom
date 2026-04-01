class Unit{
    constructor(name, hp, att){
        this.name = name;
        this.hp = hp;
        this.att = att;
    }
    attack(target){
        target.hp -= this.att;
    }
}

class Hero extends Unit{
    constructor(name, hp, att){
        super(name, hp, att);
        this.maxHp = hp;
    }
    attack(target){
        super.attack(target);
        console.log("부모 클래스의 attack() 외 추가 동작");
    }
    heal(){
        this.hp = this.maxHp;
    }
}

class Monster extends Unit {
    constructor(name, hp, att){
        super(name, hp, att);
    }
    attack(target){
        super.attack(target);
    }
}