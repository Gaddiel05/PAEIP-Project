// static/js/dashboard.js
let countrySel = document.getElementById('countrySelect');
let yearSel = document.getElementById('yearSelect');
let refreshBtn = document.getElementById('refreshBtn');

let chartPopulation, chartGDPGrowth, chartSectors, chartEmployment, chartImports, chartExports;

async function fetchJSON(url){
  const r = await fetch(url);
  return r.json();
}

async function initFilters(){
  const countries = await fetchJSON('/api/countries');
  countrySel.innerHTML = countries.map(c => `<option value="${c}">${c}</option>`).join('');
  // years
  const years = await fetchJSON('/api/years');
  yearSel.innerHTML = `<option value="">All</option>` + years.map(y => `<option value="${y}">${y}</option>`).join('');
  // set defaults
  if(countries.length) countrySel.value = countries.includes('Rwanda') ? 'Rwanda' : countries[0];
  await refresh();
}

function toFixedOrDash(v, digits=1){ return v===null || v===undefined ? '--' : Number(v).toFixed(digits);}

async function refresh(){
  const country = countrySel.value;
  const year = yearSel.value;
  const q = new URLSearchParams({country, ...(year?{year}: {})});
  const data = await fetchJSON('/api/data?' + q.toString());

  // compute KPI last available (latest year in returned data)
  if(data.length){
    const last = data[data.length-1];
    document.getElementById('kpi_nominalGDP').textContent = toFixedOrDash(last.nominalGDP,0);
    document.getElementById('kpi_fdi').textContent = toFixedOrDash(last.fdi,0);
    document.getElementById('kpi_unemployment').textContent = toFixedOrDash(last.unemployment,1);
    document.getElementById('kpi_inflation').textContent = toFixedOrDash(last.inflation,1);

    document.getElementById('kpi_imports').textContent = toFixedOrDash(last.imports,0);
    document.getElementById('kpi_exports').textContent = toFixedOrDash(last.exports,0);
    document.getElementById('kpi_ir').textContent = toFixedOrDash(last.interestRate,1);
  } else {
    ['kpi_nominalGDP','kpi_fdi','kpi_unemployment','kpi_inflation','kpi_imports','kpi_exports'].forEach(id => document.getElementById(id).textContent='--');
  }

  // prepare arrays
  const years = data.map(d=>d.year);
  const population = data.map(d=>d.population);
  const gdpGrowth = data.map(d=>d.gdpGrowth);
  const imports = data.map(d=>d.imports);
  const exports = data.map(d=>d.exports);

  // If a single-year filter: use that row's sector shares
  let sectorShares = null, employmentShares = null;
  if(data.length === 1){
    const d = data[0];
    sectorShares = [d.agricultureShare, d.servicesShare, d.industryShare, d.miningShare, d.othersShare];
    employmentShares = [d.agricultureEmployment, d.servicesEmployment, d.industryEmployment, d.miningEmployment, d.othersEmployment];
  } else if (data.length > 0){
    // take latest row for shares
    const d = data[data.length-1];
    sectorShares = [d.agricultureShare, d.servicesShare, d.industryShare, d.miningShare, d.othersShare];
    employmentShares = [d.agricultureEmployment, d.servicesEmployment, d.industryEmployment, d.miningEmployment, d.othersEmployment];
  }

  drawOrUpdateLine('chartPopulation', chartPopulation, years, population, 'Population (M)', val => val);
  drawOrUpdateLine('chartGDPGrowth', chartGDPGrowth, years, gdpGrowth, 'GDP Growth (%)', val => val);
  drawOrUpdateLine('chartImports', chartImports, years, imports, 'Imports (Millions USD)', val => val);
  drawOrUpdateLine('chartExports', chartExports, years, exports, 'Exports (Millions USD)', val => val);

  drawOrUpdatePie('chartSectors', chartSectors, ["Agriculture","Services","Industry","Mining","Others"], sectorShares);
  drawOrUpdatePie('chartEmployment', chartEmployment, ["Agriculture","Services","Industry","Mining","Others"], employmentShares);
}

function drawOrUpdateLine(canvasId, chartVar, labels, data, label, transform){
  const ctx = document.getElementById(canvasId).getContext('2d');
  const cfg = {
    type:'line',
    data: {
      labels: labels,
      datasets: [{
        label,
        data: data,
        tension: 0.3,
        fill: false,
        borderWidth: 2,
        pointRadius: 3
      }]
    },
    options: {responsive:true, scales:{y:{beginAtZero:false}}}
  };
  if(chartVar && chartVar.destroy) chartVar.destroy();
  if (labels.length === 0){
    // empty placeholder
    if(chartVar && chartVar.destroy) chartVar.destroy();
    document.getElementById(canvasId).getContext('2d').clearRect(0,0,400,300);
    return;
  }
  if(canvasId==='chartGDPGrowth') cfg.options.scales.y.beginAtZero = true;
  if(canvasId==='chartPopulation') cfg.options.scales.y.beginAtZero = true;

  const newChart = new Chart(ctx, cfg);
  if(canvasId==='chartPopulation') chartPopulation = newChart;
  if(canvasId==='chartGDPGrowth') chartGDPGrowth = newChart;
  if(canvasId==='chartImports') chartImports = newChart;
  if(canvasId==='chartExports') chartExports = newChart;
}

function drawOrUpdatePie(canvasId, chartVar, labels, data){
  const el = document.getElementById(canvasId);
  const ctx = el.getContext('2d');
  if(!data){
    if(chartVar && chartVar.destroy) chartVar.destroy();
    ctx.clearRect(0,0,el.width,el.height);
    return;
  }
  const cfg = {
    type:'doughnut',
    data:{ labels, datasets:[{ data, hoverOffset:6 }]},
    options:{responsive:true}
  };
  if(chartVar && chartVar.destroy) chartVar.destroy();
  const newChart = new Chart(ctx, cfg);
  if(canvasId==='chartSectors') chartSectors = newChart;
  if(canvasId==='chartEmployment') chartEmployment = newChart;
}

refreshBtn.addEventListener('click', refresh);
countrySel && countrySel.addEventListener('change', refresh);
yearSel && yearSel.addEventListener('change', refresh);

initFilters();
