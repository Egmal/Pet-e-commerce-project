document.getElementById('more-button').addEventListener('click', () => {
    $.get(".", function(data, status){
        console.log("Data: " + data + "\nStatus: " + status);
      });
})