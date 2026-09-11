function check(condition, message = "contract failed") {
    if (!condition)
        throw new Error(message);
}
function expectThrows(action) {
    let failed = false;
    try {
        action();
    }
    catch {
        failed = true;
    }
    check(failed, "expected an error");
}
class RealImage {
    render() { return "pixels"; }
}
class ImageProxy {
    #real;
    loads = 0;
    render() {
        if (!this.#real) {
            this.#real = new RealImage();
            this.loads += 1;
        }
        return this.#real.render();
    }
}
const proxy = new ImageProxy();
check(proxy.loads === 0);
check(proxy.render() === "pixels");
check(proxy.render() === "pixels");
check(proxy.loads === 1);
console.log("OK proxy");
export {};
