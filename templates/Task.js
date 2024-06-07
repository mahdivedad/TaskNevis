 // Task creating variable 
var Html_Dg;
// Hour variable
var Hour = new Date().getHours();
// minutes variable
var Minute = new Date().getMinutes();
// Year variable
var Year = new Date().getFullYear();
// Month variable
var Month = new Date().getMonth();
// Day variable
var Day = new Date().getDay();
// describtion of Task
var Task;
// Name of Task
var NameTask
var Time;
var date;
var Condition;
var MainMinute;
function CreateTaskFunction(){
    Html_Dg=
    '<br>'+
    '<div>'+
    'Name of Task: <input type="text" id="TaskNameinput">'+
    '</div>'+
    '<br>'+
    '<div>'+
    '<div>'+
    '<lable>'+
    'Task'+
    '</lable>'+
    '</div>'+
    '<br>'+
    '<textarea id="Task" style="width: 40%;height: 200px"></textarea>'+
    '</div>'+
    '<br>'+
    '<div>'+
    '<br>'+
    '<div>'+'Time : <input id="TimeInput">'+
    '</div>'+
    '<br>'+
    '<div>'+
    'Date : <input id="DateInput">'+
    '</div>'+
    '<br>'+
    '<div>'+
    'Condition : <select id="Condition">'+
    '<option value="Nothing">-</option>'+
    '<option value="Done">Done</option>'+
    '<option value="Doing">Doing</option>'+
    '<option value="Undone">Undone</option>'+
    '</select>'+'</div>'+
    '<br>'+'<div>'+
    '<button onclick="PutTaskFunction()">put</button>'+
    '<button onclick="DeleteTaskFunction()">delete</button>'+
    '</div>';
    document.getElementById("TaskCreatingID").innerHTML=Html_Dg;
    if(Minute<10){
        MainMinute="0"+Minute;
    }
    else{
        MainMinute=Minute;
    }
    document.getElementById("TimeInput").value=Hour+":"+MainMinute;
    document.getElementById("DateInput").value=Day+"/"+Month+"/"+Year;
}

function PutTaskFunction(){
    Task=document.getElementById("Task").value;
    date=document.getElementById("DateInput").value;
    Time=document.getElementById("TimeInput").value;
    Condition=document.getElementById("Condition").value;
    NameTask=document.getElementById("TaskNameinput").value;
    $.ajax({
        method:"POST",
        URL:"/Task/PutTaskFunction?Task="+Task+"&date="+date+"&Time="+Time+"&Condition="+Condition+"&NameTask="+NameTask,
        success:function(result){
            alert("helloworld");
        }
    })
}
function DeleteTaskFunction(){
    document.getElementById("TaskCreatingID").innerHTML="";
}