function quad(a,b,c){ // СОЗДАЕМ ФУНКЦИЮ С ПЕРЕМЕННЫМИ A B C
  if(a==0) return "Введен неправильный коэффициент!"; // ЕСЛИ НЕ ВВЕДЕН ПЕРВЫЙ КОЭФФИЦИЕНТ ИЛИ ОН РАВЕН НУЛЮ ВЫВОД - ТЕКСТА
  var D=b*b-4*a*c; // СЧИТАЕМ ДИСКРИМИНАНТ
  var x1,x2;
  if(D>0){ // ЕСЛИ БОЛЬШЕ 0 СЧИТАЕМ x1 x2, ВОЗВРАЩАЕМ В ФУНКЦИЮ PROG Значения и текст на вывод
    x1=(-b+Math.sqrt(D))/(2*a);
    x2=(-b-Math.sqrt(D))/(2*a);
    return "Коэффициенты: a="+a+", b="+b+", c="+c+"\nКорни уравнения: x1="+x1+", x2="+x2+"\nДискриминант(D)="+D+";"
  } else if(D==0){// ЕСЛИ РАВЕН 0 СЧИТАЕМ x1, ВОЗВРАЩАЕМ В ФУНКЦИЮ PROG Значения и текст на вывод
    x1=-b/(2*a);
    return "Коэффициенты: a="+a+", b="+b+", c="+c+"\nКорень уравнения: x="+x1+"\nДискриминант(D)="+D+";"
  } else if(D<0) return "Коэффициенты: a="+a+", b="+b+", c="+c+"\nКорней нет!\nДискриминант(D)="+D+";"
}
function prog(){
  var a = document.getElementById('a').value; // ПРИНИМАЕМ 3 ВВЕДЕННЫХ ЧИСЛА
  var b = document.getElementById('b').value;
  var c = document.getElementById('c').value;
  var result = quad(a,b,c); // ОТПРАВЛЯЕМ ИХ В ФУНКЦИЮ ВЫШЕ
  document.getElementById('result').textContent = result; //ВЫВОДИМ НА ЭКРАН
  document.getElementById('otvet').style.display = 'block';
}
