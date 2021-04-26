$(document).ready(function(){
        function renderChart(id, data, labels){
            // var ctx = document.getElementById('myChart').getContext('2d');
            var ctx = $('#' + id)
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sales Per Day',
                        data: data,  
                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        }

        function getSalesData(id, type){
            var url = '/analytics/sales/data/'
            var method = 'GET'
            var data = {
            "type" : type
            }
            $.ajax({
            url : url,
            method : method,
            data : data,
            success : function(responsedata){
                console.log(responsedata)
                renderChart(id, responsedata.data, responsedata.labels)
            },
            error : function(err){
                $.alert("An Error Occured !!")
            }
        })
        }
        var ChartsToRender = $('.om-render-chart')
        $.each(ChartsToRender, function(index, html){
            var $this = $(this)
            if ($this.attr('id') && $this.attr('data-type')){
                getSalesData($this.attr('id'),$this.attr('data-type'))
            }
        })

    })