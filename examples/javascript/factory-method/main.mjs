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
class PlainRenderer {
    render() { return "plain"; }
}
class JsonRenderer {
    render() { return '{"format":"json"}'; }
}
class Publisher {
    publish() { return "published:" + this.make().render(); }
}
class PlainPublisher extends Publisher {
    make() { return new PlainRenderer(); }
}
class JsonPublisher extends Publisher {
    make() { return new JsonRenderer(); }
}
check(new PlainPublisher().publish() === "published:plain");
check(new JsonPublisher().publish() === 'published:{"format":"json"}');
console.log("OK factory-method");
export {};
