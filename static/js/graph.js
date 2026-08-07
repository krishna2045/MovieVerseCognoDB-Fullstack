// graph.js – draws a simple force‑directed graph using vis.js

/**
 * drawGraph
 * @param {Object} data – {nodes: ["Movie A", "Movie B"], edges: [{from, to, label}]}
 */
function drawGraph(data) {
  const container = document.getElementById('graph');
  if (!container) return;

  // Transform nodes into vis format
  const nodes = new vis.DataSet(
    data.nodes.map((name, idx) => ({ id: idx, label: name, shape: 'ellipse' }))
  );

  // Map edge source/target names to node ids
  const nameToId = {};
  data.nodes.forEach((name, idx) => { nameToId[name] = idx; });

  const edges = new vis.DataSet(
    data.edges.map(e => ({
      from: nameToId[e.from],
      to: nameToId[e.to],
      label: e.label || '',
      arrows: 'to',
      color: { color: '#ff4c4c' }
    }))
  );

  const options = {
    layout: { improvedLayout: true },
    physics: { stabilization: false },
    interaction: { hover: true },
    nodes: { font: { color: '#fff' }, color: { background: '#1c1c1c' } },
    edges: { font: { align: 'middle', color: '#fff' } }
  };

  new vis.Network(container, { nodes, edges }, options);
}
