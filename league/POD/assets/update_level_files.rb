#!/usr/bin/env ruby

# Updates from .should to expect().to
# Also updates from .stub to allow().to receive()

# Get commandline arguments
ARGV.each do|a|
  puts "Argument: #{a}"

  if File.exist?(a)

    # Read contents of the file.
    contents = File.read(a);

    # Create backup file name
    bak = a + '.bak'
    # Make original file the backup.
    File.rename(a, bak)

    # Flag used to determine whether the file should be modified.
    prev_modified = false

    # Create array based on lines in the file.
    contents = contents.lines.to_a

    contents = contents.map do | line |
      unmodified_line = line

      # Replace this statement with a catch
      if line.include? ","

        commas = line.split(",")
        commas = commas.map do |comma|
          comma_size = comma.to_s.length
          if comma_size == 5
            comma = " " + comma
          elsif comma_size == 4
            comma = "  " + comma
          elsif comma_size == 3
            comma = "   " + comma
          elsif comma_size == 2
            comma = "    " + comma
          elsif comma_size == 1
            comma = "     " + comma
          end
          comma
        end
        commas = commas.join(",")
        commas.gsub!(/^\s{1,}/, "")
        line = commas
      end

      line
    end

    # Convert from array to string
    contents = contents.join("")
    # Write the modified contents to the file.
    File.open(a, 'w') {|file| file.write(contents) }
  end
end
