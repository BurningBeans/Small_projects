//simple javascript to fill school questionnaire
var element = document.getElementsByTagName("label");
for(var i = 0; i < element.length; i++)
{
    if(element[i].innerHTML=="同意"|| element[i].innerHTML=="是"|| element[i].innerHTML=="85%以上")//modify here to change your answer
        element[i].click();
    //console.log(element[i].innerHTML);//debug line
}
document.getElementById("btSubmit").click();//comment out if you need to fill other question fields