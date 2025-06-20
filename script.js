
function plotMatrix() {
  const a11 = parseFloat(document.getElementById("a11").value);
  const a12 = parseFloat(document.getElementById("a12").value);
  const a22 = parseFloat(document.getElementById("a22").value);

  const maxVal = Math.max(Math.abs(a11), Math.abs(a12), Math.abs(a22), 1);
  const matrix = [
    [a11 / maxVal, a12 / maxVal],
    [a12 / maxVal, a22 / maxVal]
  ];

  function shapeMatrix(a11, a12, a22) {
    const determinant = a11 * a22 - a12 * a12;
    if (determinant > 0) {
      return "Ellipse";
    } else if (determinant < 0) {
      return "Hyperbola";
    } else {
      return "Parabola";
    }
  }

  const shape = shapeMatrix(a11, a12, a22);

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

  const minZ = Math.min(...z.flat());
  const maxZ = Math.max(...z.flat());

  const data = [{
    z: z,
    x: x,
    y: y,
    type: "surface",
    colorscale: "RdBu",
    showscale: true, 
    contours: {
      z: {
        show: true,
        usecolormap: true,
        highlightcolor: "#42f5ef",
        project: { z: true }, 
        width: 2,
        start: minZ,
        end: maxZ,
        size: (maxZ - minZ)/10
      }
    }
  }];

  const layout = {
    title: `Quadratic Form Surface (${shape})`,
    scene: {
      xaxis: { title: "x", range: [-10, 10] },
      yaxis: { title: "y", range: [-10, 10] },
      zaxis: { title: "f(x,y)", range: [Math.min(-10, minZ), Math.max(10, maxZ)] },
      camera: {
        eye: { x: 0, y: -2, z: 0.5 },
        up: { x: 0, y: 0, z: 1 }
      }
    },
  };

  Plotly.newPlot("plot", data, layout);
}