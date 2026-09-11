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
class ReportBuilder {
    #title = "";
    #sections = [];
    title(value) { this.#title = value.trim(); return this; }
    add(section) { this.#sections.push(section); return this; }
    build() {
        if (!this.#title)
            throw new Error("title is required");
        return Object.freeze({
            title: this.#title,
            sections: Object.freeze([...this.#sections]),
        });
    }
}
const builder = new ReportBuilder().title("Design").add("Intent");
const report = builder.build();
builder.add("Trade-offs");
check(report.sections.length === 1);
check(report.sections[0] === "Intent");
expectThrows(() => new ReportBuilder().build());
console.log("OK builder");
export {};
