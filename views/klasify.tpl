%rebase base apptitle=apptitle
<form method="POST" id="newcat" action="#" onsubmit="return getresult();">
    Kalimat : 
	<textarea cols="100%" rows="5" name="teks" id="teks">07.27 waktu indonesia barat . situasi lalu lintas jl.jakarta sampai purwakarta terpantau ramai lancar</textarea><br/>
    <div class="formsection">
    	<input type="submit" name="save" value="Kuy"/>
    </div>
</form>
<div id="result" style="width:100%;background-color:#ccc;float:left;margin: 0em 1em;padding:8px;"></div>

<script type="text/javascript">

    function getresult(){
        var param = {}
        param["refereshKamus"] = $("#refereshKamus").val()
        param["maxTweet"] = $("#maxTweet").val()
        
        $.post('{{root}}/cekKla', param, function(data) {
            $("#result").html(data);

            console.log(data);

            // for (var i = 0; i < data.length; i++) {
            //     html = "id => "+data[i].idTweet+"<br>";
            //     html += "dari => "+data[i].dari+"<br>";
            //     html += "sampai => "+data[i].sampai+"<br>";
            //     html += "jam => "+data[i].jam+"<br>";
            //     html += "kondisi => "+data[i].kondisi+"<br>";
            //     html += "<hr>";

            //     $("#result").append(html);
               
            // }
            
        });
        return false;
    }
</script>
