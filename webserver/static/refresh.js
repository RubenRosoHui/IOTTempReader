function get_sensor(){
    $.getJSON('/sensorread/data', 
    function(data){ 
        $('#hum span').text(parseFloat(data.hum).toFixed(1)); 
        $('#temp span').text(parseFloat(data.temp).toFixed(1))
    })
    return false;     
};
$(function() {
get_sensor();
setInterval(function() {
    get_sensor();
}, 5000);
});