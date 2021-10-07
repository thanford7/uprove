
const Pages = {};

function importAll(r) {
    r.keys().forEach((key) => (Pages[key] = r(key)))
}

importAll(require.context('./modules/pages', true, /\.Page\.js$/));

export default Pages;

