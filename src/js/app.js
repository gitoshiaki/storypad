import additionCalculator from './modules/addition-calculator';
import taxCalculator from './modules/tax-calculator';

var item1Price = 400;
var item2Price = 600;
var totalPrice = additionCalculator(item1Price, item2Price);
var tax = 1.08;
var priceIncludeTax = taxCalculator(totalPrice, tax);

console.log(priceIncludeTax);
