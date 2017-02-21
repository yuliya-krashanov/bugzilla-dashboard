export class chartSettings {
    constructor(labels, data){
      this.labels = labels;

      let colors = [
              '#6CD0EA',
              '#FFDE7D',
              '#FE9ABE',
              '#4AAF5F',
              '#E63C3C',
              '#2196F3',
              '#673AB7',
              '#E91E63',
              '#009688',
              '#CDDC39',
              '#FF9800',
              '#795548',
              '#9C27B0',
              '#3F51B5',
              '#00BCD4',
              '#8BC34A',
              '#FFC107',
              '#FF5722',
              '#C62828'
      ];

      if (data.length > colors.length)
          colors = colors.concat(colors);

      this.datasets = [{
          data: data,
          backgroundColor: colors,
          hoverBackgroundColor: colors
      }];

      this.options = {
            legend: {
                position: labels.length > 5 ? 'none': 'right',
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
    }

}
