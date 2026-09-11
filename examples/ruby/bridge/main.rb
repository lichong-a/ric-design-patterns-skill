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

class EmailChannel
  def send_message(value) = "email:#{value}"
end
class SmsChannel
  def send_message(value) = "sms:#{value}"
end
class Notice
  def initialize(channel) = @channel = channel
  def deliver(value) = @channel.send_message(value)
end
class UrgentNotice < Notice
  def deliver(value) = @channel.send_message("!#{value}")
end

check(Notice.new(EmailChannel.new).deliver('hi') == 'email:hi')
check(UrgentNotice.new(SmsChannel.new).deliver('hi') == 'sms:!hi')
puts "OK bridge"
