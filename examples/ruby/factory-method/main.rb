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

class PlainRenderer
  def render = 'plain'
end
class JsonRenderer
  def render = 'json'
end
class Publisher
  def publish = "published:#{make.render}"
  protected
  def make = raise(NotImplementedError, 'implement make')
end
class PlainPublisher < Publisher
  protected
  def make = PlainRenderer.new
end
class JsonPublisher < Publisher
  protected
  def make = JsonRenderer.new
end

check(PlainPublisher.new.publish == 'published:plain')
check(JsonPublisher.new.publish == 'published:json')
puts "OK factory-method"
