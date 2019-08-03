function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `nd3.jso` to fetch the metadata for a sample
  url=`/metadata/${sample}`
  d3.json(url).then((samp)=>{
    // Use d3 to select the panel with id of `#sample-metadata`
    var metadata=d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    metadata.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    console.log(Object.entries(samp));

    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    for (let [key, value] of Object.entries(samp)) {
      metadata.append("div").text(`${key}: ${value}`);
    }

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
  })
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  url2=`/samples/${sample}`
  d3.json(url2).then((sampledata)=>{
    var year_week = sampledata.year_week;
    var y_counterfactual = sampledata.y_counterfactual;
    var y_predict=sampledata.y_predict;
    var week_sales=sampledata.week_sales;
    

    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      x: year_week,
      y: y_counterfactual,
      mode: 'line',
      name: 'counterfactual sales if tax were implemented'
     };
     var trace2 = {
      x: year_week,
      y: y_predict,
      mode: 'lines',
      name: 'predicted sales from the model'
     };
     var trace3 = {
      x: year_week,
      y: week_sales,
      mode: 'markers',
      name: 'actual sales from the data'
     };
     var data = [ trace1, trace2, trace3 ];
     var layout = {
      title:'Weekly Store Sales',
      xaxis:{
        title:"week"
        },
        yaxis:{
        title: "store weekly sales"
        }
        
     };
     Plotly.newPlot('plot', data, layout);

    // @TODO: Build a Pie Chart
//     var piedata = [{
//       values: sample_values.slice(0,10),
//       labels: otu_ids.slice(0,10),
//       type: 'pie'
//     }];
    
//     var pielayout = {
//       height: 400,
//       width: 600
//     };
    
//     Plotly.newPlot('pie', piedata, pielayout);
//     // HINT: You will need to use slice() to grab the top 10 sample_values,
//     // otu_ids, and labels (10 each).
})
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
