import { NextRequest, NextResponse } from 'next/server';
import { ALLOWED_EVENTS } from '@/lib/constants';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { event, properties, timestamp } = body;

    // Validate required fields
    if (!event) {
      return NextResponse.json(
        { error: 'Event name is required' },
        { status: 400 }
      );
    }

    // Validate event type
    if (!ALLOWED_EVENTS.includes(event)) {
      return NextResponse.json(
        { error: `Invalid event type: ${event}` },
        { status: 400 }
      );
    }

    // Prepare event data
    const eventData = {
      event,
      properties: properties || {},
      timestamp: timestamp || new Date().toISOString(),
      user_agent: request.headers.get('user-agent'),
      ip_address: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip'),
      session_id: properties?.session_id || `session_${Date.now()}`,
    };

    // Try to insert into Supabase if configured
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (supabaseUrl && supabaseServiceKey) {
      try {
        const response = await fetch(`${supabaseUrl}/rest/v1/events`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${supabaseServiceKey}`,
            'apikey': supabaseServiceKey,
          },
          body: JSON.stringify(eventData),
        });

        if (!response.ok) {
          throw new Error(`Supabase error: ${response.status}`);
        }

        return NextResponse.json({ success: true, stored: 'supabase' });
      } catch (supabaseError) {
        console.error('Supabase storage failed:', supabaseError);
        // Fall through to console logging
      }
    }

    // Fallback to console logging
    console.log('[EVENT TRACKING]', JSON.stringify(eventData, null, 2));

    return NextResponse.json({ success: true, stored: 'console' });
  } catch (error) {
    console.error('Event tracking error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Only allow POST requests
export async function GET() {
  return NextResponse.json(
    { error: 'Method not allowed' },
    { status: 405 }
  );
}