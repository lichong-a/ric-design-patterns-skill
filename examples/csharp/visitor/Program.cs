using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    private static void Check(bool condition)
    {
        if (!condition) throw new InvalidOperationException("check failed");
    }
    private static void ExpectError(Action action)
    {
        bool failed = false;
        try { action(); } catch (ArgumentException) { failed = true; }
        catch (InvalidOperationException) { failed = true; }
        catch (OverflowException) { failed = true; }
        Check(failed);
    }

    public interface INodeVisitor { string VisitText(TextNode node); string VisitNumber(NumberNode node); }
    public interface INode { string Accept(INodeVisitor visitor); }
    public sealed record TextNode(string Value) : INode { public string Accept(INodeVisitor visitor) => visitor.VisitText(this); }
    public sealed record NumberNode(int Value) : INode { public string Accept(INodeVisitor visitor) => visitor.VisitNumber(this); }
    public sealed class RenderVisitor : INodeVisitor
    {
        public string VisitText(TextNode node) => "text:" + node.Value;
        public string VisitNumber(NumberNode node) => "number:" + node.Value;
    }

    public static void Main()
    {
        var visitor = new RenderVisitor();
        Check(new TextNode("a").Accept(visitor) == "text:a");
        Check(new NumberNode(7).Accept(visitor) == "number:7");
        Console.WriteLine("OK visitor");
    }
}
