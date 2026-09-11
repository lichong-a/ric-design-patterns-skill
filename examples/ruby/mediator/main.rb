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

class Toggle
  attr_accessor :changed
  def set(value) = @changed&.call(value)
end
class SubmitButton
  attr_accessor :enabled
  def initialize = @enabled = false
end
class Dialog
  attr_reader :toggle, :submit
  def initialize
    @toggle, @submit = Toggle.new, SubmitButton.new
    @toggle.changed = ->(value) { @submit.enabled = value }
  end
end

dialog = Dialog.new
check(!dialog.submit.enabled)
dialog.toggle.set(true); check(dialog.submit.enabled)
dialog.toggle.set(false); check(!dialog.submit.enabled)
puts "OK mediator"
