var book = {
	// 设置页面是否可以编辑
	setContentEditable:function(idName,type=true){
		document.getElementById(idName).contentEditable = type;
	},
	// 获取指定ID的html内容
	getContent:function(idName){
		var content = document.getElementById("container").innerHTML;
		return content;
	},
	// method 请求类型GET or POST
	httpRequest:function({url='',method='GET',data='',
		async=true,success=function(responseText){},error=function(status){}}){
		if(url == ''){
			console.log("url is empty");
			return false;
		}
		var xmlhttp;
		if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
		  	xmlhttp=new XMLHttpRequest();
		}else{// code for IE6, IE5
		  	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
		//响应
		xmlhttp.onreadystatechange=function(){
  			if (xmlhttp.readyState==4){
  				if(xmlhttp.status==200){
  					success(xmlhttp.responseText);
  				}
  			}else{
  				error(xmlhttp.status);
  			}
  		}
		xmlhttp.open(method,url,async);
		if(method == 'GET'){
			xmlhttp.send();
		}else{

        	// HTTP头
        	xmlhttp.setRequestHeader('content-type', 'application/json');
        	
        	result = {}
        	for(k in data){
        		result[k] = data[k]
        	}
        	var pay_load = {"result":result}
			// var str = "";
			// var objLenth = Object.keys(data).length;
			// var i = 1;
			// for(let key in data){
			// 	if(i < objLenth){
			// 		str += key + "=" + data[key] + "&";
			// 	}else{
			// 		str += key + "=" + data[key];
			// 	}
			// 	i+=1;
			// }
			// var formData = new FormData();
			// for(let key in data){
			// 	formData.append(key,data[key])
			// }
			// formData.append('username', '张三');
			// formData.append('email', 'zhangsan@example.com');
			// formData.append('birthDate', 1940);

			xmlhttp.send(JSON.stringify(pay_load));
		}
	}

}