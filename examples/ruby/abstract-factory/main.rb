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

class ThemedButton
  def initialize(theme) = @theme = theme
  def draw = "#{@theme}:button"
end
class ThemedCheckbox
  def initialize(theme) = @theme = theme
  def mark = "#{@theme}:checkbox"
end
class LightFactory
  def button = ThemedButton.new('light')
  def checkbox = ThemedCheckbox.new('light')
end
class DarkFactory
  def button = ThemedButton.new('dark')
  def checkbox = ThemedCheckbox.new('dark')
end

def screen(factory) = "#{factory.button.draw}/#{factory.checkbox.mark}"

check(screen(LightFactory.new) == 'light:button/light:checkbox')
check(screen(DarkFactory.new) == 'dark:button/dark:checkbox')
puts "OK abstract-factory"
