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

require 'singleton'
class Settings
  include Singleton
  def mode = 'demo'
end

check(Settings.instance.equal?(Settings.instance))
check(Settings.instance.mode == 'demo')
expect_error { Settings.new }
puts "OK singleton"
