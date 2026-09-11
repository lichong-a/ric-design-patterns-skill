export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Report {
  readonly title: string;
  readonly sections: readonly string[];
}
class ReportBuilder {
  #title = "";
  #sections: string[] = [];
  title(value: string): this { this.#title = value.trim(); return this; }
  add(section: string): this { this.#sections.push(section); return this; }
  build(): Report {
    if (!this.#title) throw new Error("title is required");
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
