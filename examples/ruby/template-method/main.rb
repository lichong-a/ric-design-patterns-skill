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

class Importer
  def run(raw) = "<#{parse(raw.strip)}>"
  protected
  def parse(_value) = raise(NotImplementedError, 'implement parse')
end
class UpperImporter < Importer
  protected
  def parse(value) = value.upcase
end

check(UpperImporter.new.run(' hello ') == '<HELLO>')
check(UpperImporter.new.run('   ') == '<>')
puts "OK template-method"
