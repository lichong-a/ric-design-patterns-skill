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

class Locked
  def open? = false
  def coin = Unlocked.new
  def enter = self
end
class Unlocked
  def open? = true
  def coin = self
  def enter = Locked.new
end
class Gate
  def initialize = @state = Locked.new
  def open? = @state.open?
  def coin = @state = @state.coin
  def enter = @state = @state.enter
end

gate = Gate.new; check(!gate.open?)
gate.enter; check(!gate.open?)
gate.coin; check(gate.open?)
gate.coin; check(gate.open?)
gate.enter; check(!gate.open?)
puts "OK state"
