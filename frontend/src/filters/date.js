import moment from "moment";

export default function (x) {
  return moment(x).format("DD MMM YYYY");
}
