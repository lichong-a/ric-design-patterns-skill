# frozen_string_literal: true

def check(condition)
  raise 'check failed' unless condition
end

def expect_error
  failed = false
  begin
    yield
  rescue StandardError
    failed = true
  end
  check(failed)
end

class Inventory
  def reserve(quantity)
    raise ArgumentError, 'positive quantity required' unless quantity.positive?
    "reserved:#{quantity}"
  end
end
class Receipts
  def create(reservation) = "receipt:#{reservation}"
end
class Checkout
  def initialize(inventory, receipts)
    @inventory, @receipts = inventory, receipts
  end
  def place(quantity) = @receipts.create(@inventory.reserve(quantity))
end

checkout = Checkout.new(Inventory.new, Receipts.new)
check(checkout.place(2) == 'receipt:reserved:2')
expect_error { checkout.place(0) }
puts "OK facade"
