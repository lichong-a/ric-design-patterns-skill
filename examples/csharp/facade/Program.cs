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

    public sealed class Inventory
    {
        public string Reserve(int quantity)
        {
            if (quantity <= 0) throw new ArgumentException("positive quantity required");
            return "reserved:" + quantity;
        }
    }
    public sealed class Receipts { public string Create(string reservation) => "receipt:" + reservation; }
    public sealed class Checkout
    {
        private readonly Inventory inventory;
        private readonly Receipts receipts;
        public Checkout(Inventory inventory, Receipts receipts) { this.inventory = inventory; this.receipts = receipts; }
        public string Place(int quantity) => receipts.Create(inventory.Reserve(quantity));
    }

    public static void Main()
    {
        var checkout = new Checkout(new Inventory(), new Receipts());
        Check(checkout.Place(2) == "receipt:reserved:2");
        ExpectError(() => checkout.Place(0));
        Console.WriteLine("OK facade");
    }
}
