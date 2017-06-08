%rebase base apptitle=apptitle
<form method="POST" id="newcat" action="#" onsubmit="return getresult();">
    <!-- Refresh Kamus : <input type="checkbox" value="0" id="refereshKamus" name="refereshKamus" /><br> -->
    Jumlah Tweet : <input type="number" name="maxTweet" id="maxTweet" value="10" max="200" /><br>
	<!-- <textarea cols="80" rows="25" name="teks" id="teks"></textarea><br/> -->
    <div class="formsection">
    	<input type="submit" name="save" value="Submit"/>
    </div>
</form>
<div id="result" style="width:100%;background-color:#ccc;float:left;margin: 0em 1em;padding:8px;"></div>


<script type="text/javascript">
    $('#refereshKamus').change(function () {
        if ($(this).attr("checked")) {
            // checked
            $("#refereshKamus").val(1);
            return;
        }
        // not checked
        $("#refereshKamus").val(0);
    });
    

    function getresult(){
        var param = {}
        param["refereshKamus"] = $("#refereshKamus").val()
        param["maxTweet"] = $("#maxTweet").val()
        
        $.post('{{root}}/handler', param, function(data) {
            $("#result").html("");

            for (var i = 0; i < data.length; i++) {
                html = "id => "+data[i].idTweet+"<br>";
                html += "dari => "+data[i].dari+"<br>";
                html += "sampai => "+data[i].sampai+"<br>";
                html += "pukul => "+data[i].pukul+"<br>";
                html += "kondisi => "+data[i].kondisi+"<br>";
                html += "<hr>";

                $("#result").append(html);
               
            }
            
        });
        return false;
    }
</script>
