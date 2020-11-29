
export default function (x) {
  x = parseFloat(x)
    .toFixed(2)
    .replace(/\.00$/, "");
  const parts = x.toString().split(".");
  parts[0] = parts[0].replace(",", "");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join(".");
}
