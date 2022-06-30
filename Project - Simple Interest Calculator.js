
function compute()
{
  var amount = document.getElementById("amount").value;
  var year = document.getElementById("year").value;
  var returnYear = new Date().getFullYear() + parseInt(year)
  var rate = document.getElementById("rate").value; 
  if (amount <= 0)
  {
    alert("Enter a positive number")
  }
  else 
  {
  let interest = amount * year * rate /100 ;
  document.getElementById("result").innerHTML="if you deposit \<span class='values'\> " + amount + ", \<\/span\> \<br\>at an interest rate of <span class='values'> "+ rate +"&#37;.</span><br>You will receive an amount of <span class='values'>"+ interest+", </span><br> in the year <span class='values'>"+ returnYear +"</span>"
  }
   
}

function change1()
{
  var val = document.getElementById("rate");
  document.getElementById("rate-change").innerText=val.value;
}
