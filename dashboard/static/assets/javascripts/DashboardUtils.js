export class chartSettings {
    constructor(labels, data){
      this.labels = labels;

      this.datasets = [{
          data: data,
          backgroundColor: [
            '#6CD0EA',
            '#FFDE7D',
            '#FE9ABE',
            '#4AAF5F',
            '#E63C3C'
          ],
          hoverBackgroundColor: [
            '#6CD0EA',
            '#FFDE7D',
            '#FE9ABE',
            '#4AAF5F',
            '#E63C3C'
          ]
      }]
    }
}

export const PieChartOptions = {
            legend: {
                position: 'right',
                labels: {
                    fontSize: 13,
                    padding: 20,
                    boxWidth: 13,
                    fontFamily: 'Lato'
                }
            },
            tooltips: {
                backgroundColor: '#fff',
                titleFontSize: 14,
                titleFontColor: '#333',
                titleFontStyle: 'normal',
                titleMarginBottom: 12,
                titleFontFamily: 'Lato',
                bodyFontFamily: 'Lato',
                bodyFontColor: '#666',
                bodyFontSize: 14,
                cornerRadius: 0,
                displayColors: false,
                xPadding: 20,
                yPadding: 18,
                callbacks: {
                    title: (tooltips, data) => {
                        return data.labels[tooltips[0].index];
                    },
                    label: (tooltip, data) => {
                        return `Total hours: ${data.datasets[0].data[tooltip.index]}`;
                    }

                }

            },
            cutoutPercentage: 65,
        };