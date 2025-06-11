function plotMatrix() {
  const a11 = parseFloat(document.getElementById("a11").value);
  const a12 = parseFloat(document.getElementById("a12").value);
  const a22 = parseFloat(document.getElementById("a22").value);

  const matrix = [[a11, a12], [a12, a22]];

  const x = math.range(-10, 10, 0.2).toArray();
  const y = math.range(-10, 10, 0.2).toArray();
  const z = [];

  for (let i = 0; i < y.length; i++) {
    const row = [];
    for (let j = 0; j < x.length; j++) {
      const xi = x[j];
      const yi = y[i];
      const value = matrix[0][0]*xi*xi + 2*matrix[0][1]*xi*yi + matrix[1][1]*yi*yi;
      row.push(value);
    }
    z.push(row);
  }

  const data = [{
    z: z,
    x: x,
    y: y,
    type: "surface",
    colorscale: "YlGnBu",
    showscale: false
  }];

  const layout = {
    title: "Quadratic Form Surface",
    scene: {
      xaxis: { title: "x", range: [-10, 10] },
      yaxis: { title: "y", range: [-10, 10] },
      zaxis: { title: "f(x,y)", range: [-100, 100] },
    },
  };

  Plotly.newPlot("plot", data, layout);
}