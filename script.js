function scaleMatrix(matrix, scaleFactor) {
  return matrix.map(row => row.map(value => value * scaleFactor));
}

function rotateMatrix(matrix, angleDegrees) {
  const angle = angleDegrees * Math.PI / 180;
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return [
    [cos * matrix[0][0] - sin * matrix[0][1], cos * matrix[0][1] + sin * matrix[0][0]],
    [cos * matrix[1][0] - sin * matrix[1][1], cos * matrix[1][1] + sin * matrix[1][0]]
  ];
}

function shearMatrix(matrix, shearFactor) {
  return [
    [matrix[0][0] + shearFactor * matrix[0][1], matrix[0][1]],
    [matrix[1][0], matrix[1][1] + shearFactor * matrix[1][0]]
  ];
}

function shapeMatrix(a11, a12, a22) {
  const determinant = a11 * a22 - a12 * a12;
  if (determinant > 0) {
    return "Ellipse";
  } else if (determinant < 0) {
    return "Hyperbola";
  } else {
  } return "Parabola";
}

function plotMatrix() {
  const a11 = parseFloat(document.getElementById("a11").value);
  const a12 = parseFloat(document.getElementById("a12").value);
  const a22 = parseFloat(document.getElementById("a22").value);

  const shape = shapeMatrix(a11, a12, a22);

  let matrix = [
    [a11, a12],
    [a12, a22]
  ];
  if (document.getElementById("enable-scale").checked) {
    const scaleFactor = parseFloat(document.getElementById("scale").value) || 1;
    matrix = scaleMatrix(matrix, scaleFactor);
  }

  if (document.getElementById("enable-rotation").checked) {
    const rotationAngle = parseFloat(document.getElementById("rotation").value) || 0;
    matrix = rotateMatrix(matrix, rotationAngle);
  }

  if (document.getElementById("enable-shear").checked) {
    const shearFactor = parseFloat(document.getElementById("shear").value) || 0;
    matrix = shearMatrix(matrix, shearFactor);
  }

  //const maxVal = Math.max(Math.abs(a11), Math.abs(a12), Math.abs(a22), 1);
  //const matrix = [
    //[a11 / maxVal, a12 / maxVal],
    //[a12 / maxVal, a22 / maxVal]
  //];

  const maxVal = Math.max(...matrix.flat().map(Math.abs), 1);
  const normalizedMatrix = matrix.map(row => row.map(value => value / maxVal));

  visualizeMatrix(normalizedMatrix);
}

function visualizeMatrix(matrix) {
  const a11 = matrix[0][0];
  const a12 = matrix[0][1];
  const a22 = matrix[1][1];
  const shape = shapeMatrix(a11, a12, a22);

  const x = math.range(-10, 10, 0.2).toArray();
  const y = math.range(-10, 10, 0.2).toArray();
  const z = [];
  
  for (let i = 0; i < y.length; i++) {
    const row = [];
    for (let j = 0; j < x.length; j++) {
      const xi = x[j];
      const yi = y[i];
      const value = a11*xi*xi + 2*a12*xi*yi + a22*yi*yi;
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