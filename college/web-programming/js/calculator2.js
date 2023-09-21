const CALCULATOR_SCREEN = document.querySelector('table#calculator div#calculatorDisplay');
const CALCULATOR_STATUS = document.querySelector('table#calculator div#calculatorStatus');
const ARIFMETICS = ["/", "*", "**", "-", "+"];

const FIRST_NUMBER_INDEX = 0;

var numbers = ['0'];
var arifmetic = [''];

document.querySelectorAll('table#calculator button.number').forEach(button => button.addEventListener('click', ButtonNumberClick));
document.querySelectorAll('table#calculator button.edit').forEach(button => button.addEventListener('click', ButtonEditClick));
document.querySelectorAll('table#calculator button.arithmetic').forEach(button => button.addEventListener('click', ButtonArifmeticClick));
document.querySelectorAll('table#calculator button.result').forEach(button => button.addEventListener('click', ButtonResultClick));

/**
 * Обработка нажатия на кнопку калькулятора
 * Обрабатываем цифровые
 *
 * @param	Object	event	событие нажатия на кнопку
 * @return 	string
**/
function ButtonNumberClick(event)
{
	const VALUE = event.target.value;
	const CURENT_NUMBER_INDEX = numbers.length - 1;
	if (numbers[CURENT_NUMBER_INDEX] == '0') {
		numbers[CURENT_NUMBER_INDEX] = VALUE;
	} else {
		numbers[CURENT_NUMBER_INDEX] += VALUE;
	}
	ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
	return numbers[CURENT_NUMBER_INDEX];
}
/**
 * Обработка нажатия на кнопку калькулятора
 * Обрабатываем редактирование
 *
 * @param	Object	event	событие нажатия на кнопку
 * @return 	boolean
 * @todo 	delete last symbol
**/
function ButtonEditClick(event)
{
	const VALUE = event.target.value;
	const CURENT_NUMBER_INDEX = numbers.length - 1;
	switch (VALUE) {
		case 'c':
			numbers = ['0'];
			arifmetic = [''];
			ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
		break;
		
		case 'ce':
			numbers[CURENT_NUMBER_INDEX] = '0';
			ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
		break;
		
		case '<-':
	    if (numbers[CURENT_NUMBER_INDEX].length > 1) {
	        numbers[CURENT_NUMBER_INDEX] = numbers[CURENT_NUMBER_INDEX].slice(0, -1);
	    } else {
	        numbers[CURENT_NUMBER_INDEX] = '0';
	    }
	    ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
		break;
		 case 'inverse': // Обратное число ¹/X
            if (numbers[CURENT_NUMBER_INDEX] != '0') {
                numbers[CURENT_NUMBER_INDEX] = (1 / parseFloat(numbers[CURENT_NUMBER_INDEX])).toString();
                ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
            }
            break;
        
        case 'square': // Возведение в квадрат X²
            numbers[CURENT_NUMBER_INDEX] = (Math.pow(parseFloat(numbers[CURENT_NUMBER_INDEX]), 2)).toString();
            ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
            break;
        
        case 'sqrt': // Квадратный корень ²√X
            if (parseFloat(numbers[CURENT_NUMBER_INDEX]) >= 0) {
                numbers[CURENT_NUMBER_INDEX] = (Math.sqrt(parseFloat(numbers[CURENT_NUMBER_INDEX]))).toString();
                ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
            }
            break;
             case 'percent': // Процент %
            numbers[CURENT_NUMBER_INDEX] = (parseFloat(numbers[CURENT_NUMBER_INDEX]) / 100).toString();
            ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
            break;
        
        case 'changeSign': // Смена знака +/-
            numbers[CURENT_NUMBER_INDEX] = (-1 * parseFloat(numbers[CURENT_NUMBER_INDEX])).toString();
            ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
            break;
	}
}
/**
 * Обработка нажатия на кнопку калькулятора
 * Обрабатываем математические действия
 *
 * @param	Object	event	событие нажатия на кнопку
 * @return 	string
**/
function ButtonArifmeticClick(event)
{	
	const VALUE = event.target.value;
	const CURENT_NUMBER_INDEX = arifmetic.length - 1;
	
	ButtonResultClick();
	
	arifmetic[CURENT_NUMBER_INDEX] = VALUE;
	numbers.push('0');
	ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
	return arifmetic
}
/**
 * Обработка нажатия на кнопку калькулятора
 * Обрабатываем вычисление
 *
 * @param	Object	event	событие нажатия на кнопку
 * @return 	number 
 * @todo	
**/
function ButtonResultClick(event)
{
    const CURENT_NUMBER_INDEX = arifmetic.length - 1;
    switch (arifmetic[CURENT_NUMBER_INDEX]) {
        case '/':
            numbers = [(numbers[0] / numbers[1])];
            break;
        case '*':
            numbers = [(numbers[0] * numbers[1])];
            break;
        case '**':
            numbers = [Math.pow(numbers[0], numbers[1])];
            break;
        case '-':
            numbers = [(numbers[0] - numbers[1])];
            break;
        case '+':
            numbers = [(Number(numbers[0]) + Number(numbers[1]))];
            break;
    }
    arifmetic = [''];
    ShowOnScreen(CALCULATOR_SCREEN, numbers, arifmetic);
}
/**
 * Вывод на экран
 *
 * @param	object screen
 * @param	array numbers
 * @param	string arifmetic
 * @return 	number
 * @todo	use array for show
**/
function ShowOnScreen(screen, numbers, arifmetic) {
    let result = "";
    for (let i = 0; i < Math.max(numbers.length, arifmetic.length); i++) {
        if (numbers[i] != null) result += numbers[i];
        if (arifmetic[i] != null) result += ' ' + arifmetic[i] + ' ';
    }
    screen.innerHTML = result;
    return result;
}